"""
SanskritAI
Pipeline State

Stores execution information for the linguistic pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.base import BaseModel
from models.enums.pipeline_stage import PipelineStage


@dataclass
class PipelineState(BaseModel):
    """
    Represents the current execution state
    of a Sentence or Sloka.
    """

    # --------------------------------------------------
    # Current Stage
    # --------------------------------------------------

    current_stage: PipelineStage = PipelineStage.CREATED

    # --------------------------------------------------
    # Completed Stages
    # --------------------------------------------------

    completed_stages: list[PipelineStage] = field(default_factory=list)

    # --------------------------------------------------
    # Runtime Information
    # --------------------------------------------------

    started_at: datetime | None = None

    finished_at: datetime | None = None

    duration_seconds: float = 0.0

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    successful: bool = False

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    # --------------------------------------------------
    # Plugin Information
    # --------------------------------------------------

    analyzer_name: str = ""

    plugin_name: str = ""

    plugin_version: str = ""

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def start(self):

        self.started_at = datetime.utcnow()

        self.touch()

    # --------------------------------------------------

    def finish(self):

        self.finished_at = datetime.utcnow()

        if self.started_at:

            self.duration_seconds = (
                self.finished_at -
                self.started_at
            ).total_seconds()

        self.successful = True

        self.touch()

    # --------------------------------------------------

    def advance(self, stage: PipelineStage):

        self.current_stage = stage

        if stage not in self.completed_stages:
            self.completed_stages.append(stage)

        self.touch()

    # --------------------------------------------------

    def add_warning(self, message: str):

        self.warnings.append(message)

        self.touch()

    # --------------------------------------------------

    def add_error(self, message: str):

        self.errors.append(message)

        self.current_stage = PipelineStage.FAILED

        self.successful = False

        self.touch()

    # --------------------------------------------------

    @property
    def is_complete(self):

        return self.current_stage == PipelineStage.COMPLETE

    # --------------------------------------------------

    def summary(self):

        return (
            f"Pipeline("
            f"{self.current_stage.value}, "
            f"success={self.successful})"
        )
