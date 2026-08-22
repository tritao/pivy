"""Check that declarative field policies still apply to generated stubs."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

from tools.pivy_stub_typing_policy import (
    FACTORY_CLASSES,
    FIELD_ATTRIBUTE_TYPE_POLICIES,
    FIELD_TYPE_POLICIES,
    MULTIFIELD_TYPE_POLICIES,
)


def _methods(tree: ast.Module) -> dict[str, dict[str, list[ast.FunctionDef]]]:
    result: dict[str, dict[str, list[ast.FunctionDef]]] = {}
    bases: dict[str, tuple[str, ...]] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            result[node.name] = {}
            bases[node.name] = tuple(
                base.id for base in node.bases if isinstance(base, ast.Name)
            )
            for member in node.body:
                if isinstance(member, ast.FunctionDef):
                    result[node.name].setdefault(member.name, []).append(member)
    changed = True
    while changed:
        changed = False
        for class_name, class_bases in bases.items():
            for base in class_bases:
                for method_name, candidates in result.get(base, {}).items():
                    if method_name not in result[class_name]:
                        result[class_name][method_name] = candidates
                        changed = True
    return result


def _has_incomplete(node: ast.AST) -> bool:
    return any(
        isinstance(child, ast.Name) and child.id == "Incomplete"
        for child in ast.walk(node)
    )


def _check_method(
    errors: list[str],
    methods: dict[str, dict[str, list[ast.FunctionDef]]],
    class_name: str,
    method_name: str,
) -> list[ast.FunctionDef]:
    candidates = methods.get(class_name, {}).get(method_name, [])
    if not candidates:
        errors.append("%s.%s is missing" % (class_name, method_name))
    return candidates


def policy_coverage_errors(stub_path: Path) -> tuple[str, ...]:
    tree = ast.parse(stub_path.read_text(encoding="utf-8"), filename=str(stub_path))
    methods = _methods(tree)
    errors: list[str] = []

    for class_name in sorted(FACTORY_CLASSES):
        factories = _check_method(errors, methods, class_name, "createInstance")
        if any(_has_incomplete(method.returns) for method in factories):
            errors.append("%s.createInstance still contains Incomplete" % class_name)

    for class_name, field_policy in FIELD_TYPE_POLICIES.items():
        get_values = _check_method(errors, methods, class_name, "getValue")
        if any(_has_incomplete(method.returns) for method in get_values):
            errors.append("%s.getValue still contains Incomplete" % class_name)

        setters = _check_method(errors, methods, class_name, "setValue")
        if setters and all(_has_incomplete(method) for method in setters):
            errors.append("%s.setValue has no typed overload" % class_name)

    for class_name, field_policy in MULTIFIELD_TYPE_POLICIES.items():
        get_items = methods.get(class_name, {}).get("__getitem__", [])
        if any(_has_incomplete(method.returns) for method in get_items):
            errors.append("%s.__getitem__ still contains Incomplete" % class_name)

        if field_policy.indexed_access:
            set_items = _check_method(errors, methods, class_name, "__setitem__")
            if any(_has_incomplete(method) for method in set_items):
                errors.append("%s.__setitem__ still contains Incomplete" % class_name)

        iterators = _check_method(errors, methods, class_name, "__iter__")
        if any(_has_incomplete(method.returns) for method in iterators):
            errors.append("%s.__iter__ still contains Incomplete" % class_name)

        snapshots = _check_method(errors, methods, class_name, "getValuesSnapshot")
        if any(_has_incomplete(method.returns) for method in snapshots):
            errors.append(
                "%s.getValuesSnapshot still contains Incomplete" % class_name
            )

        if field_policy.set_values_types:
            setters = _check_method(errors, methods, class_name, "setValues")
            if setters and all(_has_incomplete(method) for method in setters):
                errors.append("%s.setValues has no typed overload" % class_name)

        if field_policy.get_values_type:
            getters = _check_method(errors, methods, class_name, "getValues")
            if any(_has_incomplete(method.returns) for method in getters):
                errors.append("%s.getValues still contains Incomplete" % class_name)

        if field_policy.single_value_type:
            setters = _check_method(errors, methods, class_name, "setValue")
            if setters and all(_has_incomplete(method) for method in setters):
                errors.append("%s.setValue has no typed overload" % class_name)

    for class_name, attributes in FIELD_ATTRIBUTE_TYPE_POLICIES.items():
        node = next(
            (candidate for candidate in tree.body
             if isinstance(candidate, ast.ClassDef)
             and candidate.name == class_name),
            None,
        )
        if node is None:
            errors.append("%s is missing" % class_name)
            continue
        declared = {
            item.target.id: ast.unparse(item.annotation)
            for item in node.body
            if isinstance(item, ast.AnnAssign)
            and isinstance(item.target, ast.Name)
        }
        for name, expected_type in attributes.items():
            actual_type = declared.get(name)
            if actual_type is None:
                errors.append("%s.%s is missing" % (class_name, name))
            elif actual_type != expected_type:
                errors.append(
                    "%s.%s has %s, expected %s"
                    % (class_name, name, actual_type, expected_type)
                )

    return tuple(errors)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stub", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = policy_coverage_errors(args.stub)
    if errors:
        for error in errors:
            print("error: policy coverage: %s" % error)
        return 1
    print("Pivy typing policy coverage passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
