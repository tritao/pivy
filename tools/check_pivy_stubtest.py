"""Run curated runtime parity checks against the installed SWIG module."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


CURATED_CLASSES = (
    "SoBase",
    "SoType",
    "SoField",
    "SoFieldContainer",
    "SoNode",
    "SoEngine",
    "SoMFFloat",
    "SoMFVec3f",
    "SoMFNode",
    "SoMFString",
)
CURATED_CLASSES_BY_MODULE = {
    "pivy.coin": CURATED_CLASSES,
    "pivy.gui.soqt": (
        "SoQt",
        "SoQtComponent",
        "SoQtGLWidget",
        "SoQtRenderArea",
        "SoQtViewer",
        "SoQtPopupMenu",
        "SoQtCursor",
        "SoQtKeyboard",
    ),
}


def _curated_classes(module: str) -> tuple[str, ...]:
    return CURATED_CLASSES_BY_MODULE.get(module, ())


def _class_prefixes(module: str) -> tuple[str, ...]:
    return tuple("%s.%s." % (module, name) for name in _curated_classes(module))


def curated_runtime_errors(output: str, module: str = "pivy.coin") -> tuple[str, ...]:
    """Return non-baseline stubtest errors for the reviewed public classes."""

    prefixes = _class_prefixes(module)
    errors = []
    for line in output.splitlines():
        if not line.startswith(prefixes):
            continue
        if ".__swig_destroy__ variable differs from runtime type" in line:
            # SWIG exposes this implementation detail as a builtin function;
            # its exact callable signature is not part of Pivy's API contract.
            continue
        errors.append(line)
    return tuple(errors)


def run_stubtest(module: str, root: Path) -> tuple[str, ...]:
    """Run stubtest from the build tree so the installed extension is loaded."""

    config = root / "tools" / "pivy_stubtest_mypy.ini"
    build_dir = root / "build"
    command = [
        sys.executable,
        "-m",
        "mypy.stubtest",
        "--concise",
        "--mypy-config-file",
        str(config),
        module,
    ]
    result = subprocess.run(
        command,
        cwd=build_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    output = result.stdout + result.stderr
    if "error: not checking stubs due to mypy build errors:" in output:
        raise RuntimeError(output.strip())
    if result.returncode > 1:
        raise RuntimeError(
            "stubtest failed to run for %s (exit %d):\n%s"
            % (module, result.returncode, output.strip())
        )
    return curated_runtime_errors(output, module)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", action="append")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parent.parent
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    modules = tuple(args.module or CURATED_CLASSES_BY_MODULE)
    try:
        errors = tuple(
            error
            for module in modules
            for error in run_stubtest(module, args.root)
        )
    except (OSError, RuntimeError) as error:
        print("error: %s" % error, file=sys.stderr)
        return 1
    if errors:
        print("Pivy curated stubtest failures:", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(
        "Pivy curated stubtest passed (%s)"
        % ", ".join(
            "%s: %s" % (module, ", ".join(_curated_classes(module)))
            for module in modules
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
