"""Build one typing-coverage dashboard for Pivy's public stub modules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from tools.report_pivy_typing import collect_report, report_to_dict


DEFAULT_STUBS = (
    Path("pivy/coin.pyi"),
    Path("pivy/gui/soqt.pyi"),
    Path("pivy/sogui.pyi"),
)
REPORT_SCHEMA_VERSION = 1

# These are lower/upper bounds, not exact snapshots.  Adding a concrete
# annotation is always allowed; losing one or increasing an explicitly
# budgeted boundary is a regression that needs review.
COVERAGE_BASELINES = {
    "pivy/coin.pyi": {
        "min_concrete_annotations": 21883,
        "max_any_annotations": 0,
        "max_incomplete_annotations": 417,
        "max_incomplete_categories": {
            "raw C pointers": 102,
            "callbacks": 30,
            "unknown output parameters": 0,
            "function pointers": 36,
            "dynamic/runtime API": 249,
            "uncategorized": 0,
        },
    },
    "pivy/gui/soqt.pyi": {
        "min_concrete_annotations": 745,
        "max_any_annotations": 0,
        "max_incomplete_annotations": 20,
        "max_incomplete_categories": {"uncategorized": 0},
    },
    "pivy/sogui.pyi": {
        "min_concrete_annotations": 70,
        "max_any_annotations": 1,
        "max_incomplete_annotations": 0,
        "max_incomplete_categories": {"uncategorized": 0},
    },
}


def coverage_regressions(report: dict[str, object]) -> tuple[str, ...]:
    """Return violations of the reviewed per-module coverage budgets."""

    violations = []
    for stub, baseline in COVERAGE_BASELINES.items():
        metrics = report["modules"].get(stub)
        if metrics is None:
            continue
        if metrics["concrete_annotations"] < baseline["min_concrete_annotations"]:
            violations.append(
                "%s concrete annotations dropped below %d (got %d)"
                % (
                    stub,
                    baseline["min_concrete_annotations"],
                    metrics["concrete_annotations"],
                )
            )
        if metrics["any_annotations"] > baseline["max_any_annotations"]:
            violations.append(
                "%s Any annotations exceeded %d (got %d)"
                % (stub, baseline["max_any_annotations"], metrics["any_annotations"])
            )
        if metrics["incomplete_annotations"] > baseline["max_incomplete_annotations"]:
            violations.append(
                "%s Incomplete annotations exceeded %d (got %d)"
                % (
                    stub,
                    baseline["max_incomplete_annotations"],
                    metrics["incomplete_annotations"],
                )
            )
        categories = metrics["incomplete_categories"]
        for category, maximum in baseline["max_incomplete_categories"].items():
            actual = categories[category]["count"]
            if actual > maximum:
                violations.append(
                    "%s %s Incomplete sites exceeded %d (got %d)"
                    % (stub, category, maximum, actual)
                )
    return tuple(violations)


def build_report(stubs: tuple[Path, ...] = DEFAULT_STUBS) -> dict[str, object]:
    """Return deterministic per-module typing metrics."""

    modules = {}
    for stub in stubs:
        report = collect_report(stub)
        modules[str(stub)] = report_to_dict(report, stub)
    result = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "modules": modules,
        "baselines": COVERAGE_BASELINES,
    }
    result["regressions"] = list(coverage_regressions(result))
    return result


def format_report(report: dict[str, object]) -> str:
    lines = [
        "Pivy typing coverage dashboard",
        "==============================",
        "",
        "Stub                  Concrete    Any  Incomplete  Uncategorized",
    ]
    for stub, metrics in report["modules"].items():
        lines.append(
            "%-21s %9d %6d %11d %14d"
            % (
                stub,
                metrics["concrete_annotations"],
                metrics["any_annotations"],
                metrics["incomplete_annotations"],
                metrics["incomplete_categories"]["uncategorized"]["count"],
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
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print("Wrote Pivy typing coverage report to %s" % args.output)
    else:
        sys.stdout.write(format_report(report) + "\n")

    if args.check:
        errors = []
        for stub, metrics in report["modules"].items():
            if metrics["incomplete_categories"]["uncategorized"]["count"]:
                errors.append("%s has uncategorized Incomplete sites" % stub)
        errors.extend(coverage_regressions(report))
        if errors:
            for error in errors:
                print("error: typing coverage: %s" % error, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
