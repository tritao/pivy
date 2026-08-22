"""Regenerate Pivy stubs and check them against the committed public stubs."""

from difflib import unified_diff
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STUB_GENERATOR = PROJECT_ROOT / "tools" / "generate_pivy_stubs.py"
COIN_STUBS = (Path("pivy/coin.pyi"), Path("pivy/_coin.pyi"))
SOQT_STUBS = (Path("pivy/gui/soqt.pyi"), Path("pivy/gui/_soqt.pyi"))


def regenerate(output_dir: Path, modules: tuple[str, ...]) -> None:
    stubgen = shutil.which("stubgen")
    if not stubgen:
        raise RuntimeError("stubgen is required for the stub drift check")

    command = [
        sys.executable,
        str(STUB_GENERATOR),
        "--stubgen",
        stubgen,
        "--output",
        str(output_dir),
        "--stamp",
        str(output_dir / ".pyi-stamp"),
    ]
    for module in modules:
        command.extend(("--module", module))

    environment = os.environ.copy()
    pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = os.pathsep.join(
        value for value in (str(output_dir), pythonpath) if value
    )
    result = subprocess.run(
        command,
        cwd=output_dir,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError("stub regeneration failed")


def compare_stubs(generated_dir: Path, stubs: tuple[Path, ...]) -> list[str]:
    differences = []
    for relative_path in stubs:
        committed_path = PROJECT_ROOT / relative_path
        generated_path = generated_dir / relative_path
        if not generated_path.exists():
            differences.append("missing generated stub: %s" % relative_path)
            continue

        committed = committed_path.read_text(encoding="utf-8").splitlines()
        generated = generated_path.read_text(encoding="utf-8").splitlines()
        if committed == generated:
            continue

        differences.extend(
            unified_diff(
                committed,
                generated,
                fromfile=str(relative_path),
                tofile="generated/%s" % relative_path,
                lineterm="",
            )
        )
    return differences


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="pivy-stub-drift-") as directory:
        generated_dir = Path(directory)
        build_package = PROJECT_ROOT / "build" / "pivy"
        if not build_package.exists():
            raise RuntimeError("build/pivy is required for the stub drift check")

        # CMake runs stubgen against the SWIG-generated Python modules in the
        # build tree. Seed the temporary package with that exact input so the
        # check includes generated field properties and shadow methods.
        shutil.copytree(build_package, generated_dir / "pivy")
        modules = ["pivy.coin"]
        stubs = list(COIN_STUBS)
        if (build_package / "gui" / "soqt.py").exists():
            modules.append("pivy.gui.soqt")
            stubs.extend(SOQT_STUBS)

        regenerate(generated_dir, tuple(modules))
        differences = compare_stubs(generated_dir, tuple(stubs))

    if differences:
        print("Pivy generated stubs are out of date:")
        print("\n".join(differences))
        return 1

    print("Pivy generated stubs match committed stubs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
