from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Derivation Pipeline

Canonical orchestration layer.

The pipeline coordinates SanskritAI kernels while the actual
linguistic reasoning remains inside the individual kernels.

Version
-------
v1.0.0
"""

from SanskritAI.domain.derivation.default_derivation_resolver import (
    DefaultDerivationResolver,
)
from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)
from SanskritAI.domain.pipeline.derivation_pipeline_context import (
    DerivationPipelineContext,
)
from SanskritAI.domain.pipeline.derivation_pipeline_result import (
    DerivationPipelineResult,
)
from SanskritAI.domain.pipeline.derivation_pipeline_step import (
    DerivationPipelineStep,
)
from SanskritAI.domain.pipeline.derivation_pipeline_trace import (
    DerivationPipelineTrace,
    DerivationPipelineTraceEntry,
)


class DefaultDerivationPipeline:
    """
    Canonical Morphological Derivation Pipeline.
    """

    def __init__(self) -> None:

        self._steps = (

            DerivationPipelineStep(
                identifier="pipeline.derivation",
                name="Morphological Derivation",
                kernel="Derivation",
                operation=self._run_derivation,
                priority=100,
            ),

        )

    # ---------------------------------------------------------

    @property
    def steps(self):
        return tuple(
            sorted(
                self._steps,
            )
        )

    # ---------------------------------------------------------

    def _run_derivation(
        self,
        context: DerivationPipelineContext,
        previous,
    ):
        return DefaultDerivationResolver().analyze(
            DerivationContext(
                identifier=context.identifier,
                subject=context.subject,
                dhatu=context.dhatu,
                pratyaya=context.pratyaya,
                metadata=context.metadata,
                source=context.source,
                language=context.language,
                script=context.script,
            )
        )

    # ---------------------------------------------------------

    def execute(
        self,
        context: DerivationPipelineContext,
    ) -> DerivationPipelineResult:

        trace = DerivationPipelineTrace()

        current = None

        succeeded = True

        diagnostics = []

        for step in self.steps:

            try:

                output = step.execute(
                    context,
                    current,
                )

                trace = trace.add(
                    DerivationPipelineTraceEntry(
                        step=step,
                        input_value=current,
                        output_value=output,
                        succeeded=True,
                    )
                )

                current = output

            except Exception as exc:

                succeeded = False

                diagnostics.append(str(exc))

                trace = trace.add(
                    DerivationPipelineTraceEntry(
                        step=step,
                        input_value=current,
                        output_value=None,
                        succeeded=False,
                        diagnostics=(str(exc),),
                    )
                )

                break

        confidence = (
            1.0
            if succeeded
            else 0.0
        )

        return DerivationPipelineResult(
            context=context,
            value=current,
            trace=trace,
            diagnostics=tuple(diagnostics),
            succeeded=succeeded,
            confidence=confidence,
        )
