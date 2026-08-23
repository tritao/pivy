"""Small, observable pipeline primitives for Pivy stub generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


TextTransform = Callable[[str], str]


@dataclass(frozen=True)
class Stage:
    """One named text transformation in the stub pipeline."""

    name: str
    transform: TextTransform


@dataclass(frozen=True)
class PipelineResult:
    """The transformed text and the stages that produced it."""

    text: str
    completed_stages: tuple[str, ...]


def run_pipeline(text: str, stages: tuple[Stage, ...]) -> PipelineResult:
    """Run stages in declaration order and retain an audit trail."""

    completed = []
    for stage in stages:
        text = stage.transform(text)
        completed.append(stage.name)
    return PipelineResult(text=text, completed_stages=tuple(completed))
