"""The current compatibility renderer for semantic stub models."""

from __future__ import annotations

from .model import parse_stub, render_stub


def render_pyi(text: str, module: str) -> str:
    """Validate and render a processed stub without changing its bytes."""

    return render_stub(parse_stub(text, name=module))
