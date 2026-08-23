"""The current compatibility renderer for semantic stub models."""

from __future__ import annotations

from .model import render_stub
from .resolved import ResolvedModule, resolve_stub


def render_resolved_pyi(resolved: ResolvedModule) -> str:
    """Render syntax from a resolved model without owning policy decisions."""

    return render_stub(resolved.module)


def render_pyi(text: str, module: str) -> str:
    """Resolve and render a processed stub without changing its bytes."""

    return render_resolved_pyi(resolve_stub(text, name=module))
