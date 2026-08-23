"""Audit the public sequence contract of every generated Coin multifield."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import sys

try:
    from tools.pivy_stub_typing_policy import MULTIFIELD_TYPE_POLICIES
except ImportError:
    from pivy_stub_typing_policy import MULTIFIELD_TYPE_POLICIES


@dataclass(frozen=True)
class _ClassInfo:
    bases: tuple[str, ...]
    body: tuple[ast.stmt, ...]


def _annotation(node: ast.AST | None) -> str:
    return ast.unparse(node) if node is not None else "object"


def _classes(tree: ast.Module) -> dict[str, _ClassInfo]:
    return {
        node.name: _ClassInfo(
            tuple(
                base.id for base in node.bases if isinstance(base, ast.Name)
            ),
            tuple(node.body),
        )
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }


def _methods(
    class_name: str,
    method_name: str,
    classes: dict[str, _ClassInfo],
    seen: set[str] | None = None,
) -> tuple[ast.FunctionDef, ...]:
    seen = set() if seen is None else seen
    if class_name in seen:
        return ()
    seen.add(class_name)
    info = classes.get(class_name)
    if info is None:
        return ()

    own = tuple(
        node
        for node in info.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == method_name
    )
    if own:
        return own
    inherited = []
    for base in info.bases:
        inherited.extend(_methods(base, method_name, classes, seen))
    return tuple(inherited)


def _parameters(method: ast.FunctionDef) -> tuple[tuple[str, str], ...]:
    args = [*method.args.posonlyargs, *method.args.args]
    return tuple(
        (arg.arg, _annotation(arg.annotation))
        for arg in args
        if arg.arg not in {"self", "cls"}
    )


def _return_type(method: ast.FunctionDef) -> str:
    return _annotation(method.returns)


def _has_signature(
    methods: tuple[ast.FunctionDef, ...],
    expected_parameters: tuple[tuple[str, str], ...],
    expected_return: str,
) -> bool:
    return any(
        _parameters(method) == expected_parameters
        and _return_type(method) == expected_return
        for method in methods
    )


def _has_indexed_value(
    methods: tuple[ast.FunctionDef, ...], value_types: set[str]
) -> bool:
    for method in methods:
        parameters = _parameters(method)
        if len(parameters) == 2 and parameters[0][1] == "int":
            if parameters[1][1] in value_types:
                return True
    return False


def audit(path: Path) -> tuple[list[str], int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    classes = _classes(tree)
    errors: list[str] = []

    for class_name, policy in sorted(MULTIFIELD_TYPE_POLICIES.items()):
        methods = {
            name: _methods(class_name, name, classes)
            for name in (
                "__len__",
                "__getitem__",
                "__setitem__",
                "__iter__",
                "setValues",
                "set1Value",
                "getValues",
                "getValuesSnapshot",
            )
        }
        if class_name not in classes:
            errors.append("%s is missing from %s" % (class_name, path))
            continue

        # The generated bindings use either ``i`` or ``index`` for integer
        # indexing.  Keep the check semantic while still rejecting slices.
        if not any(
            _parameters(method) in {
                (("i", "int"),),
                (("index", "int"),),
            }
            and _return_type(method) == policy.element_type
            for method in methods["__getitem__"]
        ):
            errors.append(
                "%s.__getitem__ must accept int and return %s"
                % (class_name, policy.element_type)
            )

        if not _has_signature(methods["__len__"], (), "int"):
            errors.append("%s.__len__ must return int" % class_name)

        direct_value_type = policy.single_value_type or policy.element_type
        if not _has_indexed_value(
            methods["__setitem__"], {direct_value_type}
        ):
            errors.append(
                "%s.__setitem__ must accept int and %s"
                % (class_name, direct_value_type)
            )
        if not _has_indexed_value(methods["set1Value"], {direct_value_type}):
            errors.append(
                "%s.set1Value must accept int and %s"
                % (class_name, direct_value_type)
            )

        if not _has_signature(
            methods["__iter__"], (), "Iterator[%s]" % policy.element_type
        ):
            errors.append(
                "%s.__iter__ must return Iterator[%s]"
                % (class_name, policy.element_type)
            )
        if not _has_signature(
            methods["getValuesSnapshot"],
            (),
            "list[%s]" % policy.element_type,
        ):
            errors.append(
                "%s.getValuesSnapshot must return list[%s]"
                % (class_name, policy.element_type)
            )

        get_values_type = policy.get_values_type or policy.element_type
        if not any(
            _parameters(method) in {
                (("i", "int"),),
                (("start", "int"),),
            }
            and _return_type(method) == "list[%s]" % get_values_type
            for method in methods["getValues"]
        ):
            errors.append(
                "%s.getValues must return list[%s]"
                % (class_name, get_values_type)
            )

        expected_set_values = {
            tuple((name, annotation) for name, annotation in parameters)
            for parameters in (
                (("values", "Sequence[%s]" % value_type),)
                for value_type in policy.set_values_types
            )
        }
        expected_set_values.update(
            tuple(
                (name, annotation)
                for name, annotation in (
                    ("start", "int"),
                    ("values", "Sequence[%s]" % value_type),
                )
            )
            for value_type in policy.set_values_types
        )
        expected_set_values.update(
            tuple(
                (name, annotation)
                for name, annotation in (
                    ("start", "int"),
                    ("num", "int"),
                    ("values", "Sequence[%s]" % value_type),
                )
            )
            for value_type in policy.set_values_types
        )
        actual_set_values = {
            _parameters(method)
            for method in methods["setValues"]
            if _return_type(method) == "None"
        }
        missing_set_values = sorted(expected_set_values - actual_set_values)
        for signature in missing_set_values:
            errors.append(
                "%s.setValues is missing (%s) -> None"
                % (class_name, ", ".join("%s: %s" % item for item in signature))
            )

        for method_name in ("__getitem__", "__setitem__"):
            if any(
                "slice" in annotation
                for method in methods[method_name]
                for _, annotation in _parameters(method)
            ):
                errors.append(
                    "%s.%s unexpectedly exposes slice semantics"
                    % (class_name, method_name)
                )

    return errors, len(MULTIFIELD_TYPE_POLICIES)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    path = Path(arguments[0]) if arguments else Path("pivy/coin.pyi")
    errors, count = audit(path)
    if errors:
        print("Pivy multifield consistency failed")
        for error in errors:
            print("- %s" % error)
        return 1
    print(
        "Pivy multifield consistency passed (%d policy families; slices unsupported)"
        % count
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
