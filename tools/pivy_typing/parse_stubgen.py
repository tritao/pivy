"""Input boundary for raw stubgen output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StubgenOutput:
    module: str
    path: Path
    text: str


def read_stubgen_output(path: str | Path, module: str) -> StubgenOutput | None:
    """Read a stubgen result, returning ``None`` when it was not emitted."""

    stub_path = Path(path)
    if not stub_path.exists():
        return None
    return StubgenOutput(
        module=module,
        path=stub_path,
        text=stub_path.read_text(encoding="utf-8"),
    )
