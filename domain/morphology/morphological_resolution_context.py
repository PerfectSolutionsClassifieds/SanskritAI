from __future__ import annotations

"""
SanskritAI
==========

Morphological Resolution Context

Defines the canonical context consumed by the Morphological
Resolution Kernel.

The existing MorphologicalContext represents the complete
execution context for morphological analysis. This class provides
the explicit resolution-layer name required by the Morphological
Resolution Kernel and Strategy.

Architecture
------------

ResolutionContext
        │
        ▼
MorphologicalResolutionContext
        │
        ▼
MorphologicalResolutionKernel
        │
        ▼
MorphologicalResolutionStrategy
        │
        ▼
MorphologicalAnalyzer

Design
------

MorphologicalResolutionContext intentionally extends the existing
MorphologicalContext rather than duplicating its fields.

This preserves the existing MorphologicalContext as the canonical
morphology execution context while giving the resolution layer a
precise domain type.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.morphological_context import (
    MorphologicalContext,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MorphologicalResolutionContext(
    MorphologicalContext,
):
    """
    Canonical resolution context for the Morphology Kernel.

    No additional state is introduced.

    The class exists to provide a precise type boundary between
    the general morphological execution context and the
    resolution kernel.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Morphological Resolution Context"

    @property
    def display_text(
        self,
    ) -> str:
        return self.word_form.display_text

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Canonical context supplied to the "
            "Morphological Resolution Kernel."
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
