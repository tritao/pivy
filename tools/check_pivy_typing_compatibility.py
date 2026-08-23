"""Check a curated, source-level compatibility snapshot for Pivy stubs."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = PROJECT_ROOT / "tests" / "pivy_typing_compatibility.json"

MODULE_PATHS = {
    "pivy.coin": Path("pivy") / "coin.pyi",
    "pivy.gui.soqt": Path("pivy") / "gui" / "soqt.pyi",
    "pivy.sogui": Path("pivy") / "sogui.pyi",
}


@dataclass(frozen=True)
class MethodSignature:
    parameters: tuple[tuple[str, str], ...]
    return_type: str


@dataclass(frozen=True)
class ClassInfo:
    bases: tuple[str, ...]
    methods: dict[str, tuple[MethodSignature, ...]]
    attributes: dict[str, str]


@dataclass(frozen=True)
class ModuleInfo:
    classes: dict[str, ClassInfo]
    aliases: dict[str, str]


def annotation_text(annotation: ast.expr | None) -> str:
    return ast.unparse(annotation) if annotation is not None else "Any"


def method_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> MethodSignature:
    arguments = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    if arguments and arguments[0].arg in {"self", "cls"}:
        arguments = arguments[1:]
    parameters = tuple(
        (argument.arg, annotation_text(argument.annotation))
        for argument in arguments
    )
    return MethodSignature(parameters, annotation_text(node.returns))


def class_info(node: ast.ClassDef) -> ClassInfo:
    methods: dict[str, list[MethodSignature]] = {}
    attributes: dict[str, str] = {}
    for member in node.body:
        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.setdefault(member.name, []).append(method_signature(member))
        elif isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name):
            attributes[member.target.id] = annotation_text(member.annotation)
    return ClassInfo(
        bases=tuple(annotation_text(base) for base in node.bases),
        methods={name: tuple(signatures) for name, signatures in methods.items()},
        attributes=attributes,
    )


def parse_module(path: Path) -> ModuleInfo:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    classes = {
        node.name: class_info(node)
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }
    aliases = {
        node.targets[0].id: ast.unparse(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and isinstance(node.value, (ast.Name, ast.Attribute, ast.Subscript))
    }
    return ModuleInfo(classes=classes, aliases=aliases)


def effective_method(
    classes: dict[str, ClassInfo], class_name: str, method_name: str
) -> tuple[MethodSignature, ...] | None:
    seen: set[str] = set()

    def visit(name: str) -> tuple[MethodSignature, ...] | None:
        if name in seen:
            return None
        seen.add(name)
        info = classes.get(name)
        if info is None:
            return None
        if method_name in info.methods:
            return info.methods[method_name]
        for base in info.bases:
            found = visit(base)
            if found is not None:
                return found
        return None

    return visit(class_name)


def effective_attribute(
    classes: dict[str, ClassInfo], class_name: str, attribute_name: str
) -> str | None:
    seen: set[str] = set()

    def visit(name: str) -> str | None:
        if name in seen:
            return None
        seen.add(name)
        info = classes.get(name)
        if info is None:
            return None
        if attribute_name in info.attributes:
            return info.attributes[attribute_name]
        for base in info.bases:
            found = visit(base)
            if found is not None:
                return found
        return None

    return visit(class_name)


def expected_signature(value: dict[str, Any]) -> MethodSignature:
    return MethodSignature(
        tuple((item["name"], item["type"]) for item in value["parameters"]),
        value["return"],
    )


def check_snapshot(
    snapshot_path: Path = SNAPSHOT_PATH,
    project_root: Path = PROJECT_ROOT,
) -> list[str]:
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if snapshot.get("schema_version") != 1:
        return ["unsupported compatibility snapshot schema"]

    errors: list[str] = []
    for module_name, expected_module in snapshot["modules"].items():
        relative_path = MODULE_PATHS.get(module_name)
        if relative_path is None:
            errors.append("%s: no stub path is registered" % module_name)
            continue
        path = project_root / relative_path
        if not path.exists():
            errors.append("%s: missing stub %s" % (module_name, relative_path))
            continue
        info = parse_module(path)
        for class_name, expected_class in expected_module.get("classes", {}).items():
            actual_class = info.classes.get(class_name)
            if actual_class is None:
                errors.append("%s.%s: missing class" % (module_name, class_name))
                continue
            expected_bases = tuple(expected_class.get("bases", []))
            if actual_class.bases != expected_bases:
                errors.append(
                    "%s.%s: bases %r, expected %r"
                    % (module_name, class_name, actual_class.bases, expected_bases)
                )
            for method_name, expected_overloads in expected_class.get(
                "methods", {}
            ).items():
                actual = effective_method(info.classes, class_name, method_name)
                expected = tuple(expected_signature(item) for item in expected_overloads)
                if actual is None:
                    errors.append(
                        "%s.%s.%s: missing method" % (module_name, class_name, method_name)
                    )
                elif actual != expected:
                    errors.append(
                        "%s.%s.%s: signature %r, expected %r"
                        % (module_name, class_name, method_name, actual, expected)
                    )
            for attribute_name, expected_type in expected_class.get(
                "attributes", {}
            ).items():
                actual_type = effective_attribute(info.classes, class_name, attribute_name)
                if actual_type != expected_type:
                    errors.append(
                        "%s.%s.%s: type %r, expected %r"
                        % (
                            module_name,
                            class_name,
                            attribute_name,
                            actual_type,
                            expected_type,
                        )
                    )
        for alias_name, expected_target in expected_module.get("aliases", {}).items():
            actual_target = info.aliases.get(alias_name)
            if actual_target != expected_target:
                errors.append(
                    "%s.%s: target %r, expected %r"
                    % (module_name, alias_name, actual_target, expected_target)
                )
    return errors


def main() -> int:
    errors = check_snapshot()
    if errors:
        print("Pivy typing compatibility snapshot failed:")
        print("\n".join("- " + error for error in errors))
        return 1
    print("Pivy typing compatibility snapshot passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
