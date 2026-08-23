"""Normalization-stage runner for the stubgen compatibility pipeline."""

from __future__ import annotations

from .pipeline import PipelineResult, Stage, run_pipeline


def apply_normalization(text: str, stages: tuple[Stage, ...]) -> PipelineResult:
    """Apply syntax and representation normalizers in a named stage group."""

    return run_pipeline(text, stages)
