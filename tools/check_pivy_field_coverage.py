"""Check generated field attributes against Coin's runtime field registry."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys

from tools.pivy_stub_typing_policy import FIELD_ATTRIBUTE_NAME_ALIASES


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _class_map(stub_path: Path) -> dict[str, ast.ClassDef]:
    tree = ast.parse(stub_path.read_text(encoding="utf-8"), filename=str(stub_path))
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }


def _bases(classes: dict[str, ast.ClassDef], class_name: str) -> tuple[str, ...]:
    node = classes.get(class_name)
    if node is None:
        return ()
    return tuple(
        base.id for base in node.bases if isinstance(base, ast.Name)
    )


def _annotations(
    classes: dict[str, ast.ClassDef],
    class_name: str,
    seen: set[str] | None = None,
) -> dict[str, str]:
    """Return annotations inherited by one generated stub class."""

    seen = set() if seen is None else seen
    if class_name in seen:
        return {}
    seen.add(class_name)

    result: dict[str, str] = {}
    for base in _bases(classes, class_name):
        result.update(_annotations(classes, base, seen))

    node = classes.get(class_name)
    if node is None:
        return result
    for member in node.body:
        if isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name):
            result[member.target.id] = ast.unparse(member.annotation)
    return result


def _load_coin():
    """Import the installed native module rather than the source stub package."""

    sys.path = [
        entry
        for entry in sys.path
        if entry not in {"", str(PROJECT_ROOT)}
    ]
    from pivy import coin

    return coin


def _silence_native_stderr():
    """Return a context manager that hides noisy Coin catalog diagnostics."""

    class NativeStderr:
        def __enter__(self):
            self.saved = os.dup(2)
            self.devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(self.devnull, 2)

        def __exit__(self, exc_type, exc_value, traceback):
            os.dup2(self.saved, 2)
            os.close(self.saved)
            os.close(self.devnull)

    return NativeStderr()


def field_coverage_errors(stub_path: Path) -> tuple[str, ...]:
    """Return typed runtime fields absent or mistyped in the generated stub."""

    classes = _class_map(stub_path)
    coin = _load_coin()
    errors: list[str] = []
    inspected_classes = 0
    inspected_fields = 0
    constructor_failures = 0
    aliases = 0
    collisions = 0

    with _silence_native_stderr():
        for class_name in sorted(classes):
            runtime_class = getattr(coin, class_name, None)
            if not isinstance(runtime_class, type):
                continue
            try:
                is_field_container = issubclass(
                    runtime_class, coin.SoFieldContainer
                )
            except TypeError:
                continue
            if not is_field_container:
                continue

            try:
                instance = runtime_class()
                field_data = instance.getFieldData()
            except Exception:
                # Abstract classes and engines requiring constructor arguments
                # are covered through their concrete subclasses or the static
                # policy checks.  They cannot provide a runtime inventory here.
                constructor_failures += 1
                continue
            if field_data is None:
                continue
            inspected_classes += 1
            static_annotations = _annotations(classes, class_name)
            for index in range(field_data.getNumFields()):
                field_name = str(field_data.getFieldName(index))
                field_value = instance.__getattr__(field_name)
                field_type = type(field_value).__name__
                if not (
                    field_type.startswith("SoSF")
                    or field_type.startswith("SoMF")
                ):
                    continue

                # A native field whose name collides with a Python method is
                # not addressable as a typed attribute (for example
                # SoDepthBuffer.write). Keep this binding limitation visible.
                if callable(getattr(runtime_class, field_name, None)):
                    collisions += 1
                    continue

                inspected_fields += 1
                expected_name = FIELD_ATTRIBUTE_NAME_ALIASES.get(
                    (class_name, field_name), field_name
                )
                if expected_name != field_name:
                    aliases += 1
                annotation = static_annotations.get(expected_name)
                if annotation is None:
                    errors.append(
                        "%s.%s is missing (runtime type %s)"
                        % (class_name, field_name, field_type)
                    )
                elif annotation != field_type:
                    errors.append(
                        "%s.%s is %s, expected %s"
                        % (class_name, expected_name, annotation, field_type)
                    )

    print(
        "Field attribute coverage: %d classes, %d typed runtime fields; "
        "%d constructor-limited classes, %d aliases, %d name collisions"
        % (
            inspected_classes,
            inspected_fields,
            constructor_failures,
            aliases,
            collisions,
        )
    )
    return tuple(errors)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stub", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = field_coverage_errors(args.stub)
    if errors:
        for error in errors:
            print("error: field coverage: %s" % error)
        return 1
    print("Pivy runtime field attributes are covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
