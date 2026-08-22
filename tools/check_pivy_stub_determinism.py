"""Check that Pivy stub postprocessing is idempotent."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile

from tools.generate_pivy_stubs import postprocess_stub


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_PACKAGE = PROJECT_ROOT / "build" / "pivy"
MODULE_STUBS = (
    ("pivy.coin", Path("coin.pyi")),
    ("pivy.gui.soqt", Path("gui") / "soqt.pyi"),
)


def main() -> int:
    if not BUILD_PACKAGE.exists():
        print("error: build/pivy is required for the stub determinism check", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="pivy-stub-determinism-") as directory:
        output_dir = Path(directory)
        package_dir = output_dir / "pivy"
        shutil.copytree(BUILD_PACKAGE, package_dir)

        for module, relative_stub in MODULE_STUBS:
            path = package_dir / relative_stub
            if not path.exists():
                if module == "pivy.gui.soqt":
                    continue
                print("error: missing generated stub: %s" % relative_stub, file=sys.stderr)
                return 1

            postprocess_stub(str(path), module, str(output_dir))
            first_pass = path.read_bytes()
            postprocess_stub(str(path), module, str(output_dir))
            second_pass = path.read_bytes()
            if first_pass != second_pass:
                print("error: postprocessing is not idempotent for %s" % module, file=sys.stderr)
                return 1

    print("Pivy stub postprocessing is deterministic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
