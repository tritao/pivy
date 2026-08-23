"""Canonical, backend-neutral representation of a Pivy stub model."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from .model import Class, Module, Overload, Parameter, TypeExpr, parse_stub


MANIFEST_SCHEMA_VERSION = 1


def _canonical_type(type_expr: TypeExpr | None) -> str | None:
    """Normalize annotation spelling while retaining unknown expressions."""

    if type_expr is None:
        return None
    try:
        return ast.unparse(ast.parse(type_expr.text, mode="eval").body)
    except SyntaxError:
        # A future producer may emit a valid annotation syntax that this
        # interpreter does not understand.  A trimmed source spelling is a
        # better comparison value than dropping the type altogether.
        return type_expr.text.strip()


def _parameter_manifest(parameter: Parameter) -> dict[str, Any]:
    return {
        "default": parameter.default,
        "kind": parameter.kind,
        "name": parameter.name,
        "type": _canonical_type(parameter.type),
    }


def _overload_manifest(overload: Overload) -> dict[str, Any]:
    return {
        "parameters": [
            _parameter_manifest(parameter)
            for parameter in overload.parameters
            if parameter.name not in {"self", "cls"}
        ],
        "return": _canonical_type(overload.return_type),
    }


def _class_manifest(class_: Class) -> dict[str, Any]:
    return {
        "attributes": {
            attribute.name: _canonical_type(attribute.type)
            for attribute in class_.attributes
        },
        "bases": [_canonical_type(base) for base in class_.bases],
        "methods": {
            method.name: {
                "decorators": list(method.decorators),
                "overloads": [
                    _overload_manifest(overload)
                    for overload in method.overloads
                ],
            }
            for method in class_.methods
        },
    }


def module_to_manifest(module: Module) -> dict[str, Any]:
    """Convert a semantic model into a deterministic JSON-compatible value."""

    return {
        "classes": {
            class_.name: _class_manifest(class_)
            for class_ in module.classes
        },
        "module": module.name,
        "schema_version": MANIFEST_SCHEMA_VERSION,
    }


def render_manifest(manifest: dict[str, Any]) -> str:
    """Render a canonical manifest with stable ordering and a final newline."""

    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def manifest_from_stub(stub_path: Path) -> dict[str, Any]:
    """Parse a stub file and return its canonical manifest."""

    source = stub_path.read_text(encoding="utf-8")
    return module_to_manifest(parse_stub(source, name=str(stub_path)))


def _diff_values(left: Any, right: Any, path: str) -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        differences = []
        for key in sorted(left.keys() - right.keys()):
            differences.append("%s: removed %r" % (path + "." + key, left[key]))
        for key in sorted(right.keys() - left.keys()):
            differences.append("%s: added %r" % (path + "." + key, right[key]))
        for key in sorted(left.keys() & right.keys()):
            differences.extend(_diff_values(left[key], right[key], path + "." + key))
        return differences

    if isinstance(left, list) and isinstance(right, list):
        differences = []
        common_length = min(len(left), len(right))
        for index in range(common_length):
            differences.extend(_diff_values(left[index], right[index], "%s[%d]" % (path, index)))
        for index in range(common_length, len(left)):
            differences.append("%s[%d]: removed %r" % (path, index, left[index]))
        for index in range(common_length, len(right)):
            differences.append("%s[%d]: added %r" % (path, index, right[index]))
        return differences

    if left != right:
        return ["%s: %r != %r" % (path, left, right)]
    return []


def manifest_diff(left: dict[str, Any], right: dict[str, Any]) -> tuple[str, ...]:
    """Return stable, structural differences between two manifests."""

    return tuple(_diff_values(left, right, "$"))


__all__ = [
    "MANIFEST_SCHEMA_VERSION",
    "manifest_diff",
    "manifest_from_stub",
    "module_to_manifest",
    "render_manifest",
]
