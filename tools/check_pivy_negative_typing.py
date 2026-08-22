"""Assert that intentionally invalid Pivy typing examples stay invalid."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
NEGATIVE_TEST = ROOT / "tests" / "typecheck_negative" / "invalid_contracts.py"


def run_checker(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    checkers = {
        "pyright": ["pyright", "--warnings", str(NEGATIVE_TEST)],
        "pyrefly": [
            "pyrefly",
            "check",
            "--summary=none",
            "--search-path",
            ".",
            str(NEGATIVE_TEST),
        ],
    }
    failures = []
    for name, command in checkers.items():
        returncode, output = run_checker(command)
        if returncode == 0:
            failures.append("%s accepted invalid_contracts.py" % name)
            continue
        print("%s rejected invalid_contracts.py as expected" % name)
    if failures:
        for failure in failures:
            print("error: %s" % failure, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
