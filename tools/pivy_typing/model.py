"""A lossless, initially small semantic model for generated Pivy stubs.

Phase 1 intentionally keeps the model boring.  It records the public classes,
methods, overloads, parameters and attributes that later pipeline stages will
need, while retaining the original source as the compatibility representation.
That lets us put a real model in the generation path before making rendering a
semantic change.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


class _StubSource:
    """Provide source segments without rescanning the complete module."""

    def __init__(self, text: str):
        self.text = text
        self.lines = text.splitlines(keepends=True)

    @staticmethod
    def _slice(line: str, start: int, end: int) -> str:
        # AST column offsets are UTF-8 byte offsets, rather than character
        # offsets.  Using bytes keeps source extraction correct for docstrings
        # and comments containing non-ASCII text as well.
        encoded = line.encode("utf-8")
        return encoded[start:end].decode("utf-8")

    def segment(self, node: ast.AST | None) -> str | None:
        if node is None:
            return None
        if not all(
            hasattr(node, attribute)
            for attribute in ("lineno", "col_offset", "end_lineno", "end_col_offset")
        ):
            return ast.unparse(node)

        start_line = self.lines[node.lineno - 1]
        end_line = self.lines[node.end_lineno - 1]
        if node.lineno == node.end_lineno:
            return self._slice(start_line, node.col_offset, node.end_col_offset)

        parts = [self._slice(start_line, node.col_offset, None)]
        parts.extend(self.lines[node.lineno : node.end_lineno - 1])
        parts.append(self._slice(end_line, 0, node.end_col_offset))
        return "".join(parts)


@dataclass(frozen=True)
class TypeExpr:
    """A Python type expression preserved in source form."""

    text: str


@dataclass(frozen=True)
class Parameter:
    """One callable parameter and its source-level annotation/default."""

    name: str
    type: TypeExpr | None
    default: str | None
    kind: str


@dataclass(frozen=True)
class Overload:
    """The signature portion of a method definition."""

    parameters: tuple[Parameter, ...]
    return_type: TypeExpr | None


@dataclass(frozen=True)
class Method:
    """A method, including all definitions used to express overloads."""

    name: str
    overloads: tuple[Overload, ...]
    decorators: tuple[str, ...]
    line: int


@dataclass(frozen=True)
class Attribute:
    """An annotated class attribute."""

    name: str
    type: TypeExpr | None
    line: int


@dataclass(frozen=True)
class Class:
    """A public class declaration in a stub module."""

    name: str
    bases: tuple[TypeExpr, ...]
    methods: tuple[Method, ...]
    attributes: tuple[Attribute, ...]
    line: int


@dataclass(frozen=True)
class Module:
    """The semantic view of a stub module.

    ``source`` is retained deliberately.  Until the semantic renderer is
    introduced, returning it is the byte-for-byte compatibility guarantee for
    architecture-only changes.
    """

    name: str
    source: str
    classes: tuple[Class, ...]


def _source_segment(source: _StubSource, node: ast.AST | None) -> str | None:
    return source.segment(node)


def _type_expr(source: _StubSource, node: ast.AST | None) -> TypeExpr | None:
    segment = _source_segment(source, node)
    return None if segment is None else TypeExpr(segment)


def _parameter_nodes(
    args: ast.arguments,
) -> tuple[tuple[str, ast.arg, str], ...]:
    """Return parameters with their public kind in declaration order."""

    positional_only = tuple(
        (arg.arg, arg, "positional_only") for arg in args.posonlyargs
    )
    positional = tuple((arg.arg, arg, "positional_or_keyword") for arg in args.args)
    vararg = () if args.vararg is None else ((args.vararg.arg, args.vararg, "var_positional"),)
    keyword_only = tuple(
        (arg.arg, arg, "keyword_only") for arg in args.kwonlyargs
    )
    kwarg = () if args.kwarg is None else ((args.kwarg.arg, args.kwarg, "var_keyword"),)
    return positional_only + positional + vararg + keyword_only + kwarg


def _parse_overload(
    source: _StubSource,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> Overload:
    args = node.args
    parameters = _parameter_nodes(args)
    positional_defaults = (None,) * (
        len(args.posonlyargs) + len(args.args) - len(args.defaults)
    ) + tuple(_source_segment(source, default) for default in args.defaults)
    defaults_by_name = {
        arg.arg: default
        for (arg, default) in zip(
            args.posonlyargs + args.args,
            positional_defaults,
        )
    }
    keyword_defaults = {
        arg.arg: _source_segment(source, default)
        for arg, default in zip(args.kwonlyargs, args.kw_defaults)
    }

    parsed_parameters = tuple(
        Parameter(
            name=name,
            type=_type_expr(source, arg.annotation),
            default=(
                defaults_by_name.get(name)
                if kind in {"positional_only", "positional_or_keyword"}
                else keyword_defaults.get(name)
            ),
            kind=kind,
        )
        for name, arg, kind in parameters
    )
    return Overload(
        parameters=parsed_parameters,
        return_type=_type_expr(source, node.returns),
    )


def _parse_class(source: _StubSource, node: ast.ClassDef) -> Class:
    methods_by_name: dict[str, list[Overload]] = {}
    decorators_by_name: dict[str, list[str]] = {}
    method_lines: dict[str, int] = {}
    attributes: list[Attribute] = []

    for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods_by_name.setdefault(child.name, []).append(
                _parse_overload(source, child)
            )
            decorators = [
                _source_segment(source, decorator) or ""
                for decorator in child.decorator_list
            ]
            decorators_by_name.setdefault(child.name, []).extend(decorators)
            method_lines.setdefault(child.name, child.lineno)
        elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            attributes.append(
                Attribute(
                    name=child.target.id,
                    type=_type_expr(source, child.annotation),
                    line=child.lineno,
                )
            )

    methods = tuple(
        Method(
            name=name,
            overloads=tuple(overloads),
            decorators=tuple(dict.fromkeys(decorators_by_name[name])),
            line=method_lines[name],
        )
        for name, overloads in methods_by_name.items()
    )
    return Class(
        name=node.name,
        bases=tuple(_type_expr(source, base) for base in node.bases if base is not None),
        methods=methods,
        attributes=tuple(attributes),
        line=node.lineno,
    )


def parse_stub(source: str, name: str = "<memory>") -> Module:
    """Parse a Python stub into the Phase 1 semantic model."""

    source_text = _StubSource(source)
    tree = ast.parse(source, filename=name, mode="exec")
    classes = tuple(
        _parse_class(source_text, node)
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    )
    return Module(name=name, source=source, classes=classes)


def render_stub(module: Module) -> str:
    """Render a module without changing its source during Phase 1."""

    return module.source
