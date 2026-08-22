"""Run the public typing contracts against supported Python targets."""

from __future__ import annotations

import subprocess
import sys


SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12", "3.13", "3.14")


def main() -> int:
    for version in SUPPORTED_PYTHON_VERSIONS:
        print("Checking Pyright Python target %s" % version, flush=True)
        result = subprocess.run(
            [
                "pyright",
                "--pythonversion",
                version,
                "--warnings",
                "tests/typecheck",
            ]
        )
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
