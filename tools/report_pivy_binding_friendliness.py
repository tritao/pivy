"""Report who owns the remaining complexity in the Pivy/Coin API surface."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

from tools.pivy_typing.remediation import (
    REMEDIATION_CLASS_LABELS,
    RemediationRecord,
    remediation_for_boundary,
    remediation_for_callback_contract,
    remediation_for_method_contract,
)
from tools.pivy_typing.coin_api_roadmap import COIN_API_CANDIDATE_REVIEWS
from tools.pivy_typing.resolved import resolve_stub


REMEDIATION_CODES = tuple(item.value for item in REMEDIATION_CLASS_LABELS)
REPORT_SCHEMA_VERSION = 1


def _module_name(stub_path: Path) -> str:
    if stub_path.name == "coin.pyi":
        return "pivy.coin"
    if stub_path.name == "soqt.pyi":
        return "pivy.gui.soqt"
    return stub_path.stem


def _record_manifest(record: RemediationRecord) -> dict[str, str]:
    return {
        "code": record.code,
        "label": record.label,
        "confidence": record.confidence,
        "rationale": record.rationale,
        "next_action": record.next_action,
        "source": record.source,
    }


def _boundary_manifest(boundary, record: RemediationRecord) -> dict[str, object]:
    return {
        "category": boundary.category,
        "class": boundary.class_name,
        "kind": boundary.kind,
        "method": boundary.method_name,
        "name": boundary.name,
        "reason": boundary.reason,
        "source": boundary.source,
        "line": boundary.line,
        "remediation": _record_manifest(record),
    }


def _method_contract_manifest(contract, record: RemediationRecord) -> dict[str, object]:
    return {
        "kind": "method",
        "class": contract.target.class_name,
        "method": contract.target.method_name,
        "owner": contract.owner.value,
        "source": contract.source,
        "remediation": _record_manifest(record),
    }


def _callback_contract_manifest(contract, record: RemediationRecord) -> dict[str, object]:
    return {
        "kind": "callback",
        "class": contract.class_name,
        "method": contract.method_name,
        "source": contract.source,
        "remediation": _record_manifest(record),
    }


def _coin_api_review_manifest(review) -> dict[str, object]:
    return {
        "class": review.class_name,
        "method": review.method_name,
        "decision": review.classification.value,
        "owner": REMEDIATION_CLASS_LABELS[review.classification],
        "confidence": "reviewed",
        "native_signatures": list(review.native_signatures),
        "source_headers": list(review.source_headers),
        "evidence": review.evidence,
        "coin4_action": review.coin4_action,
        "coin5_direction": review.coin5_direction,
        "source": review.source,
    }


def _count_records(records: list[dict[str, object]]) -> dict[str, int]:
    counts = Counter(
        record["remediation"]["code"]
        for record in records
    )
    return {code: counts[code] for code in REMEDIATION_CODES}


def _confidence_counts(records: list[dict[str, object]]) -> dict[str, int]:
    counts = Counter(
        record["remediation"]["confidence"]
        for record in records
    )
    return dict(sorted(counts.items()))


def _code_confidence_counts(records: list[dict[str, object]]) -> dict[str, dict[str, int]]:
    counts = {
        code: {"reviewed": 0, "provisional": 0}
        for code in REMEDIATION_CODES
    }
    for record in records:
        remediation = record["remediation"]
        counts[remediation["code"]][remediation["confidence"]] += 1
    return counts


def _coin_candidates(
    boundaries: list[dict[str, object]],
    limit: int | None = None,
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for boundary in boundaries:
        if boundary["remediation"]["code"] != "C":
            continue
        method = boundary["method"] or "<attribute>"
        grouped[(boundary["class"], method)].append(boundary)

    candidates = []
    for (class_name, method_name), items in grouped.items():
        score = sum(
            {"return": 3, "parameter": 2, "attribute": 1}[item["kind"]]
            for item in items
        )
        candidates.append(
            {
                "class": class_name,
                "method": method_name,
                "score": score,
                "boundary_count": len(items),
                "categories": sorted({item["category"] for item in items}),
                "confidence": sorted(
                    {item["remediation"]["confidence"] for item in items}
                ),
                "next_actions": sorted(
                    {item["remediation"]["next_action"] for item in items}
                ),
            }
        )
    candidates.sort(key=lambda item: (-item["score"], item["class"], item["method"]))
    return candidates if limit is None else candidates[:limit]


def build_report(stub_path: Path, *, candidate_limit: int = 20) -> dict[str, object]:
    """Build a deterministic binding-friendliness report from the resolved model."""

    source = stub_path.read_text(encoding="utf-8")
    resolved = resolve_stub(source, name=_module_name(stub_path))
    boundaries = [
        _boundary_manifest(boundary, remediation_for_boundary(boundary))
        for boundary in resolved.incomplete_boundaries
    ]
    boundaries.sort(
        key=lambda item: (
            item["kind"],
            item["class"],
            item["method"] or "",
            item["name"],
        )
    )
    method_contracts = [
        _method_contract_manifest(
            contract,
            remediation_for_method_contract(contract),
        )
        for contract in resolved.method_contracts
    ]
    method_contracts.sort(key=lambda item: (item["class"], item["method"]))
    callback_contracts = [
        _callback_contract_manifest(
            contract,
            remediation_for_callback_contract(contract),
        )
        for contract in resolved.callback_contracts
    ]
    callback_contracts.sort(key=lambda item: (item["class"], item["method"]))

    special_contracts = [*method_contracts, *callback_contracts]
    boundary_categories = Counter(item["category"] for item in boundaries)
    coin_api_queue = _coin_candidates(boundaries)
    coin_api_reviews = [
        _coin_api_review_manifest(review)
        for review in COIN_API_CANDIDATE_REVIEWS
    ]
    reviewed_owner_counts = Counter(item["decision"] for item in coin_api_reviews)
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "module": resolved.name,
        "stub": str(stub_path),
        "summary": {
            "boundaries": len(boundaries),
            "boundary_categories": dict(sorted(boundary_categories.items())),
            "boundary_remediation": _count_records(boundaries),
            "boundary_confidence": _confidence_counts(boundaries),
            "boundary_confidence_by_class": _code_confidence_counts(boundaries),
            "special_contracts": len(special_contracts),
            "special_contract_remediation": _count_records(special_contracts),
            "special_contract_confidence": _confidence_counts(special_contracts),
            "special_contract_confidence_by_class": _code_confidence_counts(special_contracts),
            "reviewed_coin_api_candidates": len(coin_api_reviews),
            "reviewed_coin_api_owners": {
                code: reviewed_owner_counts[code]
                for code in REMEDIATION_CODES
            },
        },
        "coin_api_candidates": coin_api_queue[:candidate_limit],
        "coin_api_queue": coin_api_queue,
        "coin_api_reviews": coin_api_reviews,
        "boundaries": boundaries,
        "special_contracts": special_contracts,
    }


def format_report(report: dict[str, object], candidate_limit: int) -> str:
    summary = report["summary"]
    lines = [
        "Coin binding-friendliness report",
        "================================",
        "",
        "Module                           %s" % report["module"],
        "Boundaries                       %d" % summary["boundaries"],
        "Special contracts               %d" % summary["special_contracts"],
        "Reviewed Coin API candidates     %d" % summary["reviewed_coin_api_candidates"],
        "Complete Coin API queue          %d" % len(report["coin_api_queue"]),
        "",
        "Boundary remediation ownership",
        "------------------------------",
        "Class  Owner                          Count  Confidence",
    ]
    for code in REMEDIATION_CODES:
        confidence = summary["boundary_confidence_by_class"][code]
        lines.append(
            "%-6s %-30s %5d  reviewed=%d provisional=%d"
            % (
                code,
                REMEDIATION_CLASS_LABELS[next(item for item in REMEDIATION_CLASS_LABELS if item.value == code)],
                summary["boundary_remediation"][code],
                confidence["reviewed"],
                confidence["provisional"],
            )
        )
    lines.extend(
        [
            "",
            "Boundary categories",
            "-------------------",
        ]
    )
    lines.extend(
        "%5d  %s" % (count, category)
        for category, count in summary["boundary_categories"].items()
    )
    lines.extend(
        [
            "",
            "Highest-impact Coin API candidates",
            "-----------------------------------",
            "Score  Boundary  Symbol",
        ]
    )
    for candidate in report["coin_api_candidates"][:candidate_limit]:
        lines.append(
            "%5d  %8d  %s.%s"
            % (
                candidate["score"],
                candidate["boundary_count"],
                candidate["class"],
                candidate["method"],
            )
        )
    lines.extend(
        [
            "",
            "Reviewed Coin API ownership",
            "---------------------------",
            "A=%d  B=%d  C=%d  D=%d"
            % tuple(
                summary["reviewed_coin_api_owners"][code]
                for code in REMEDIATION_CODES
            ),
            "See docs/coin-api-typing-roadmap.md for declarations, evidence and actions.",
            "",
            "Special contracts",
            "-----------------",
            "Method contracts                 %d"
            % sum(item["kind"] == "method" for item in report["special_contracts"]),
            "Callback contracts               %d"
            % sum(item["kind"] == "callback" for item in report["special_contracts"]),
            "",
            "Classification is complete for all boundaries and special contracts.",
            "Reviewed entries are backed by policy, audit or roadmap records;",
            "provisional entries are the next review queue.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stub", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--check-coverage", action="store_true")
    parser.add_argument("--top", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.stub, candidate_limit=max(args.top, 0))
    if args.as_json:
        output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    else:
        output = format_report(report, max(args.top, 0)) + "\n"

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print("Wrote Coin binding-friendliness report to %s" % args.output)
    else:
        sys.stdout.write(output)

    if args.check_coverage:
        summary = report["summary"]
        if summary["boundaries"] == 0 or summary["special_contracts"] == 0:
            print("error: binding-friendliness report has no classified records", file=sys.stderr)
            return 1
        if set(summary["boundary_remediation"]) != set(REMEDIATION_CODES):
            print("error: binding-friendliness remediation classes are incomplete", file=sys.stderr)
            return 1
        boundary_symbols = {
            (item["class"], item["method"])
            for item in report["boundaries"]
        }
        missing_reviews = [
            "%s.%s" % (item["class"], item["method"])
            for item in report["coin_api_reviews"]
            if (item["class"], item["method"]) not in boundary_symbols
        ]
        if missing_reviews:
            print(
                "error: Coin API roadmap entries are absent from the resolved boundary model: %s"
                % ", ".join(missing_reviews),
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
