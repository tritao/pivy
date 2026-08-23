"""Policy-stage runner for Pivy-specific typing corrections."""

from __future__ import annotations

from .pipeline import PipelineResult, Stage, run_pipeline


def apply_policy(text: str, stages: tuple[Stage, ...]) -> PipelineResult:
    """Apply Pivy semantic policy corrections in a named stage group."""

    return run_pipeline(text, stages)
