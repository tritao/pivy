"""Report Pyright's package-level type completeness for supported Pivy modules."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import shutil
import subprocess
import sys
from typing import Iterable


DEFAULT_MODULES = (
    "pivy.coin",
    "pivy.gui.soqt",
    "pivy.sogui",
    "pivy.qt",
    "pivy.qt.QtCore",
    "pivy.qt.QtGui",
    "pivy.qt.QtOpenGL",
    "pivy.qt.QtWidgets",
)


@dataclass(frozen=True)
class VerifyTypesBaseline:
    """Reviewed lower and upper bounds for one package completeness report."""

    min_score: float
    min_known_symbols: int
    max_ambiguous_symbols: int
    max_unknown_symbols: int


# Pyright's verifytypes command is intentionally report-oriented here.  These
# are the first checked-in snapshots, not the long-term target.  The contract
# suite and generated-stub quality report remain the stricter correctness
# gates; this inventory gives package-wide work a measurable direction.
VERIFYTYPES_BASELINES = {
    "pivy.coin": VerifyTypesBaseline(
        min_score=61.0,
        min_known_symbols=8416,
        max_ambiguous_symbols=0,
        max_unknown_symbols=5385,
    ),
    "pivy.gui.soqt": VerifyTypesBaseline(
        min_score=75.4,
        min_known_symbols=399,
        max_ambiguous_symbols=0,
        max_unknown_symbols=130,
    ),
    "pivy.sogui": VerifyTypesBaseline(
        min_score=43.6,
        min_known_symbols=24,
        max_ambiguous_symbols=4,
        max_unknown_symbols=27,
    ),
    "pivy.qt": VerifyTypesBaseline(
        min_score=100.0,
        min_known_symbols=740,
        max_ambiguous_symbols=0,
        max_unknown_symbols=0,
    ),
    "pivy.qt.QtCore": VerifyTypesBaseline(
        min_score=100.0,
        min_known_symbols=235,
        max_ambiguous_symbols=0,
        max_unknown_symbols=0,
    ),
    "pivy.qt.QtGui": VerifyTypesBaseline(
        min_score=100.0,
        min_known_symbols=262,
        max_ambiguous_symbols=0,
        max_unknown_symbols=0,
    ),
    "pivy.qt.QtOpenGL": VerifyTypesBaseline(
        min_score=100.0,
        min_known_symbols=45,
        max_ambiguous_symbols=0,
        max_unknown_symbols=0,
    ),
    "pivy.qt.QtWidgets": VerifyTypesBaseline(
        min_score=100.0,
        min_known_symbols=198,
        max_ambiguous_symbols=0,
        max_unknown_symbols=0,
    ),
}


@dataclass(frozen=True)
class VerifyTypesReport:
    module: str
    exported_symbols: int
    known_symbols: int
    ambiguous_symbols: int
    unknown_symbols: int
    completeness_score: float
    pyright_returncode: int


def _summary_block(module: str, output: str) -> str:
    marker = 'Symbols exported by "%s":' % module
    start = output.find(marker)
    if start < 0:
        raise ValueError("Pyright output has no exported-symbol summary for %s" % module)
    end = output.find("Other symbols referenced", start)
    return output[start:] if end < 0 else output[start:end]


def _summary_value(block: str, label: str) -> int:
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith(label + ":"):
            value = stripped[len(label) + 1 :].strip()
            return int(value)
    raise ValueError("Pyright output has no %s summary" % label)


def parse_verifytypes_output(
    module: str,
    output: str,
    *,
    pyright_returncode: int = 0,
) -> VerifyTypesReport:
    """Parse the stable summary emitted by ``pyright --verifytypes``."""

    block = _summary_block(module, output)
    score_marker = "Type completeness score:"
    score_line = next(
        (line.strip() for line in output.splitlines() if line.strip().startswith(score_marker)),
        None,
    )
    if score_line is None:
        raise ValueError("Pyright output has no type completeness score")
    score_text = score_line[len(score_marker) :].strip()
    if not score_text.endswith("%"):
        raise ValueError("Pyright completeness score is not a percentage")

    return VerifyTypesReport(
        module=module,
        exported_symbols=_summary_value(block, "Symbols exported by \"%s\"" % module),
        known_symbols=_summary_value(block, "With known type"),
        ambiguous_symbols=_summary_value(block, "With ambiguous type"),
        unknown_symbols=_summary_value(block, "With unknown type"),
        completeness_score=float(score_text[:-1]),
        pyright_returncode=pyright_returncode,
    )


def run_verifytypes(module: str, executable: str = "pyright") -> VerifyTypesReport:
    """Run Pyright and parse its summary, including expected diagnostic exit 1."""

    command = [executable, "--verifytypes", module, "--ignoreexternal"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    report = parse_verifytypes_output(
        module,
        output,
        pyright_returncode=result.returncode,
    )
    if result.returncode > 1:
        raise RuntimeError(
            "Pyright failed to run for %s (exit %d)" % (module, result.returncode)
        )
    return report


def verifytypes_regressions(
    report: VerifyTypesReport,
    baseline: VerifyTypesBaseline | None = None,
) -> tuple[str, ...]:
    """Return violations of a reviewed package completeness baseline."""

    baseline = baseline or VERIFYTYPES_BASELINES.get(report.module)
    if baseline is None:
        return ()

    violations = []
    if report.completeness_score < baseline.min_score:
        violations.append(
            "%s completeness score dropped below %.1f%% (got %.1f%%)"
            % (report.module, baseline.min_score, report.completeness_score)
        )
    if report.known_symbols < baseline.min_known_symbols:
        violations.append(
            "%s known symbols dropped below %d (got %d)"
            % (report.module, baseline.min_known_symbols, report.known_symbols)
        )
    if report.ambiguous_symbols > baseline.max_ambiguous_symbols:
        violations.append(
            "%s ambiguous symbols exceeded %d (got %d)"
            % (report.module, baseline.max_ambiguous_symbols, report.ambiguous_symbols)
        )
    if report.unknown_symbols > baseline.max_unknown_symbols:
        violations.append(
            "%s unknown symbols exceeded %d (got %d)"
            % (report.module, baseline.max_unknown_symbols, report.unknown_symbols)
        )
    return tuple(violations)


def report_to_dict(report: VerifyTypesReport) -> dict[str, object]:
    """Return stable, JSON-serializable verifytypes data."""

    return {
        "schema_version": 1,
        "module": report.module,
        "exported_symbols": report.exported_symbols,
        "known_symbols": report.known_symbols,
        "ambiguous_symbols": report.ambiguous_symbols,
        "unknown_symbols": report.unknown_symbols,
        "completeness_score": report.completeness_score,
        "pyright_returncode": report.pyright_returncode,
    }


def format_report(reports: Iterable[VerifyTypesReport]) -> str:
    lines = [
        "Pivy package typing completeness",
        "=================================",
        "",
        "Module              Score   Exported   Known   Ambiguous   Unknown",
    ]
    for report in reports:
        lines.append(
            "%-19s %5.1f%% %9d %7d %10d %8d"
            % (
                report.module,
                report.completeness_score,
                report.exported_symbols,
                report.known_symbols,
                report.ambiguous_symbols,
                report.unknown_symbols,
            )
        )
    lines.extend(
        [
            "",
            "The score is an inventory, not a promise that native opaque boundaries are safe.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "modules",
        nargs="*",
        default=DEFAULT_MODULES,
        help="modules to inspect (default: %(default)s)",
    )
    parser.add_argument(
        "--check-baseline",
        action="store_true",
        help="fail if a reviewed module baseline regresses",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="write one stable machine-readable JSON object per module",
    )
    parser.add_argument(
        "--pyright",
        default="pyright",
        help="Pyright executable to invoke",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    executable = shutil.which(args.pyright) or args.pyright
    reports = []
    for module in args.modules:
        try:
            reports.append(run_verifytypes(module, executable))
        except (OSError, RuntimeError, ValueError) as error:
            print("error: %s" % error, file=sys.stderr)
            return 1

    if args.as_json:
        print(json.dumps([report_to_dict(report) for report in reports], indent=2, sort_keys=True))
    else:
        print(format_report(reports))

    if args.check_baseline:
        violations = [
            violation
            for report in reports
            for violation in verifytypes_regressions(report)
        ]
        if violations:
            for violation in violations:
                print("error: verifytypes baseline: %s" % violation, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
