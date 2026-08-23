"""Report typing progress by public Pivy API domain."""

from __future__ import annotations

import argparse
import ast
import json
from collections import defaultdict
from pathlib import Path
import sys

from tools.report_pivy_typing import method_parameters


DEFAULT_STUBS = (
    Path("pivy/coin.pyi"),
    Path("pivy/gui/soqt.pyi"),
    Path("pivy/sogui.pyi"),
)
DOMAIN_ORDER = (
    "values",
    "fields",
    "scenegraph",
    "actions",
    "callbacks",
    "sensors",
    "soqt",
    "sogui",
    "other",
)


def domain_for(stub: Path, class_name: str) -> str:
    """Assign a stable, intentionally broad ownership domain."""

    if stub.name == "soqt.pyi":
        return "soqt"
    if stub.name == "sogui.pyi":
        return "sogui"
    if class_name.startswith(("Sb", "SoBaseKit")):
        return "values"
    if class_name.startswith(("SoSF", "SoMF")):
        return "fields"
    if class_name.endswith("Action") or class_name.endswith("ActionP"):
        return "actions"
    if "Callback" in class_name:
        return "callbacks"
    if class_name.endswith("Sensor") or "Sensor" in class_name:
        return "sensors"
    if class_name.startswith(("SoNode", "SoGroup", "SoPath", "SoShape")):
        return "scenegraph"
    return "other"


def _site_counts(
    annotation_sites: list[tuple[str, ast.expr]],
) -> dict[str, int]:
    counts = {
        "annotation_sites": len(annotation_sites),
        "concrete_annotations": 0,
        "any_annotations": 0,
        "incomplete_annotations": 0,
    }
    for _, annotation in annotation_sites:
        names = {
            node.id
            for node in ast.walk(annotation)
            if isinstance(node, ast.Name)
        }
        if "Incomplete" in names:
            counts["incomplete_annotations"] += 1
        elif "Any" in names:
            counts["any_annotations"] += 1
        else:
            counts["concrete_annotations"] += 1
    return counts


def build_report(stubs: tuple[Path, ...] = DEFAULT_STUBS) -> dict[str, object]:
    """Return deterministic class/method/annotation progress by domain."""

    metrics: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "classes": 0,
            "methods": 0,
            "parameters": 0,
            "annotation_sites": 0,
            "concrete_annotations": 0,
            "any_annotations": 0,
            "incomplete_annotations": 0,
        }
    )
    for stub in stubs:
        tree = ast.parse(stub.read_text(encoding="utf-8"), filename=str(stub))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            domain = domain_for(stub, node.name)
            target = metrics[domain]
            target["classes"] += 1
            for member in node.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    target["methods"] += 1
                    target["parameters"] += len(method_parameters(member))
                    sites = [
                        ("parameter", parameter.annotation)
                        for parameter in method_parameters(member)
                        if parameter.annotation is not None
                    ]
                    if member.returns is not None:
                        sites.append(("return", member.returns))
                    counts = _site_counts(sites)
                elif isinstance(member, ast.AnnAssign) and member.annotation is not None:
                    counts = _site_counts([("attribute", member.annotation)])
                else:
                    continue
                for key, value in counts.items():
                    target[key] += value

    domains = {}
    for domain in DOMAIN_ORDER:
        domains[domain] = dict(metrics[domain])
    totals = {
        key: sum(domain[key] for domain in domains.values())
        for key in next(iter(domains.values()))
    }
    return {
        "schema_version": 1,
        "domains": domains,
        "totals": totals,
    }


def format_report(report: dict[str, object]) -> str:
    lines = [
        "Pivy typing progress by domain",
        "==============================",
        "",
        "Domain        Classes  Methods  Annotations  Concrete  Any  Incomplete",
    ]
    for domain, metrics in report["domains"].items():
        lines.append(
            "%-13s %7d %8d %12d %9d %4d %11d"
            % (
                domain,
                metrics["classes"],
                metrics["methods"],
                metrics["annotation_sites"],
                metrics["concrete_annotations"],
                metrics["any_annotations"],
                metrics["incomplete_annotations"],
            )
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("stubs", nargs="*", type=Path, default=DEFAULT_STUBS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(tuple(args.stubs))
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
        print("Wrote Pivy typing domain report to %s" % args.output)
    else:
        sys.stdout.write(format_report(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
