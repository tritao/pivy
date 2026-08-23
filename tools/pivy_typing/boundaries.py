"""Resolved semantic records for intentionally incomplete API boundaries."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from tools.pivy_stub_typing_policy import classify_incomplete
except ImportError:
    from pivy_stub_typing_policy import classify_incomplete

from .model import Module


@dataclass(frozen=True)
class IncompleteBoundary:
    """One ``Incomplete`` annotation resolved to a reviewed category."""

    kind: str
    class_name: str
    method_name: str | None
    name: str
    line: int
    category: str


def _has_raw_pointer_note(lines: list[str], line: int) -> bool:
    index = line - 2
    while index >= 0:
        stripped = lines[index].strip()
        if stripped and not stripped.startswith(("#", "@")):
            return False
        if "raw C pointers" in lines[index]:
            return True
        index -= 1
    return False


def _is_incomplete(type_expr) -> bool:
    return type_expr is not None and "Incomplete" in type_expr.text


def resolve_incomplete_boundaries(module: Module) -> tuple[IncompleteBoundary, ...]:
    """Resolve all incomplete annotations in a semantic stub model."""

    lines = module.source.splitlines()
    boundaries: list[IncompleteBoundary] = []
    for class_model in module.classes:
        for attribute in class_model.attributes:
            if not _is_incomplete(attribute.type):
                continue
            category = classify_incomplete(
                kind="attribute",
                class_name=class_model.name,
                method_name=None,
                parameter_name=attribute.name,
                has_raw_pointer_note=_has_raw_pointer_note(lines, attribute.line),
            )
            boundaries.append(
                IncompleteBoundary(
                    kind="attribute",
                    class_name=class_model.name,
                    method_name=None,
                    name=attribute.name,
                    line=attribute.line,
                    category=category,
                )
            )

        for method in class_model.methods:
            for overload in method.overloads:
                if _is_incomplete(overload.return_type):
                    category = classify_incomplete(
                        kind="return",
                        class_name=class_model.name,
                        method_name=method.name,
                        parameter_name="return",
                        has_raw_pointer_note=_has_raw_pointer_note(
                            lines, overload.line
                        ),
                    )
                    boundaries.append(
                        IncompleteBoundary(
                            kind="return",
                            class_name=class_model.name,
                            method_name=method.name,
                            name="return",
                            line=overload.line,
                            category=category,
                        )
                    )
                for parameter in overload.parameters:
                    if not _is_incomplete(parameter.type):
                        continue
                    category = classify_incomplete(
                        kind="parameter",
                        class_name=class_model.name,
                        method_name=method.name,
                        parameter_name=parameter.name,
                        has_raw_pointer_note=_has_raw_pointer_note(
                            lines, parameter.line
                        ),
                    )
                    boundaries.append(
                        IncompleteBoundary(
                            kind="parameter",
                            class_name=class_model.name,
                            method_name=method.name,
                            name=parameter.name,
                            line=parameter.line,
                            category=category,
                        )
                    )
    return tuple(boundaries)
