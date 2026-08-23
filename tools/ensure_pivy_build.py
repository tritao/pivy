"""Build Pivy without forcing an unnecessary CMake reconfigure."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = PROJECT_ROOT / "build"


def configure_command(project_root: Path, install_prefix: str) -> list[str]:
    """Return the first-build CMake command used by the Pixi build task."""

    return [
        "cmake",
        "-G",
        "Ninja",
        "-B",
        str(project_root / "build"),
        "-S",
        str(project_root),
        "-D",
        "CMAKE_BUILD_TYPE=Release",
        "-D",
        "CMAKE_INSTALL_PREFIX:FILEPATH=%s" % install_prefix,
        "-D",
        "CMAKE_PREFIX_PATH=%s" % install_prefix,
        "-D",
        "PIVY_USE_QT6:BOOL=ON",
        "-D",
        "PIVY_USE_SOQT:BOOL=ON",
        "-D",
        "QT_HOST_PATH=%s" % install_prefix,
    ]


def build_command(project_root: Path, jobs: int = 10) -> list[str]:
    """Return the incremental Ninja install command."""

    return [
        "ninja",
        "-C",
        str(project_root / "build"),
        "-j",
        str(jobs),
        "install",
    ]


def ensure_build(
    project_root: Path = PROJECT_ROOT,
    *,
    install_prefix: str | None = None,
    jobs: int = 10,
) -> None:
    """Configure only when needed, then build and install incrementally.

    Ninja still performs its normal dependency and CMake-input checks. The
    important distinction is that an existing ``build.ninja`` is not preceded
    by an unconditional CMake invocation, which avoids the SWIG wrapper churn
    caused by the project's configure-time glob checks.
    """

    root = project_root.resolve()
    build_dir = root / "build"
    prefix = install_prefix or os.environ.get("CONDA_PREFIX") or sys.prefix
    if not (build_dir / "build.ninja").exists():
        subprocess.run(
            configure_command(root, prefix),
            cwd=root,
            check=True,
        )

    subprocess.run(build_command(root, jobs), cwd=root, check=True)


def main() -> int:
    ensure_build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
