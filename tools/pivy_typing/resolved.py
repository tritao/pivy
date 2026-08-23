"""Resolved semantic view consumed by Pivy typing backends."""

from __future__ import annotations

from dataclasses import dataclass

from .boundaries import IncompleteBoundary, resolve_incomplete_boundaries
from .callbacks import CallbackContract, callback_contracts_for_module
from .model import Class, Module, parse_stub


@dataclass(frozen=True)
class ResolvedModule:
    """Semantic model plus binding-policy decisions for one stub module."""

    module: Module
    incomplete_boundaries: tuple[IncompleteBoundary, ...]
    callback_contracts: tuple[CallbackContract, ...]

    @property
    def name(self) -> str:
        return self.module.name

    @property
    def source(self) -> str:
        return self.module.source

    @property
    def classes(self) -> tuple[Class, ...]:
        return self.module.classes


def resolve_module(module: Module) -> ResolvedModule:
    """Apply all currently modeled semantic boundary and callback policy."""

    class_names = {class_.name for class_ in module.classes}
    callback_contracts = tuple(
        contract
        for contract in callback_contracts_for_module(module.name)
        if contract.class_name in class_names
    )
    return ResolvedModule(
        module=module,
        incomplete_boundaries=resolve_incomplete_boundaries(module),
        callback_contracts=callback_contracts,
    )


def resolve_stub(source: str, name: str = "<memory>") -> ResolvedModule:
    """Parse and resolve a stub in one backend-independent operation."""

    return resolve_module(parse_stub(source, name=name))


__all__ = ["ResolvedModule", "resolve_module", "resolve_stub"]
