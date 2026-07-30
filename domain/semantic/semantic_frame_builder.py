from __future__ import annotations

"""
SanskritAI
==========

Semantic Frame Builder

Converts upstream kernel outputs into structured semantic
frames.

This helper makes it easy for semantic rules to produce
concepts, relations, and frames from Vakya, Derivation, and
Grammar outputs.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.semantic.semantic_concept import SemanticConcept
from SanskritAI.domain.semantic.semantic_frame import SemanticFrame
from SanskritAI.domain.semantic.semantic_relation import SemanticRelation


class SemanticFrameBuilder:
    """
    Builds structured semantic frames from upstream outputs.
    """

    @staticmethod
    def _as_text(value: Any) -> str:
        if value is None:
            return ""
        if hasattr(value, "display_text"):
            return str(getattr(value, "display_text"))
        return str(value)

    @staticmethod
    def _extract_text(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, dict):
            for key in ("text", "sentence", "surface", "meaning", "value"):
                if key in value and value[key] is not None:
                    return str(value[key]).strip()
        if hasattr(value, "subject"):
            return str(getattr(value, "subject"))
        if hasattr(value, "display_text"):
            return str(getattr(value, "display_text"))
        return str(value).strip()

    @staticmethod
    def concept(
        identifier: str,
        name: str,
        gloss: str = "",
        category: str = "",
        description: str = "",
    ) -> SemanticConcept:
        return SemanticConcept(
            identifier=identifier,
            name=name,
            gloss=gloss,
            category=category,
            description=description,
        )

    @staticmethod
    def relation(
        identifier: str,
        relation: str,
        source: SemanticConcept,
        target: SemanticConcept,
        confidence: float = 1.0,
        notes: str = "",
    ) -> SemanticRelation:
        return SemanticRelation(
            identifier=identifier,
            relation=relation,
            source=source,
            target=target,
            confidence=confidence,
            notes=notes,
        )

    def from_upstream(
        self,
        identifier: str,
        label: str,
        upstream: Any,
        *,
        role: str = "",
        confidence: float = 0.90,
        notes: str = "",
    ) -> SemanticFrame:
        """
        Builds a frame from a single upstream output.
        """
        text = self._extract_text(upstream)

        source_concept = self.concept(
            identifier=f"{identifier}:source",
            name=label,
            gloss=text,
            category=role or "upstream",
            description=notes,
        )

        target_concept = self.concept(
            identifier=f"{identifier}:target",
            name="Meaning",
            gloss=self._as_text(getattr(upstream, "best_output", None) or getattr(upstream, "best_analysis", None) or upstream),
            category="meaning",
            description="Derived semantic target",
        )

        relation = self.relation(
            identifier=f"{identifier}:rel:1",
            relation=role or "derives-from",
            source=source_concept,
            target=target_concept,
            confidence=confidence,
            notes=notes,
        )

        return SemanticFrame(
            identifier=identifier,
            label=label,
            concepts=(source_concept, target_concept),
            relations=(relation,),
            summary=f"{label}: {text}",
            confidence=confidence,
            notes=notes,
        )

    def from_vakya(
        self,
        identifier: str,
        vakya: Any,
    ) -> SemanticFrame:
        return self.from_upstream(
            identifier=identifier,
            label="Vakya Meaning Frame",
            upstream=vakya,
            role="sentence",
            confidence=0.92,
            notes="Frame built from Vakya output.",
        )

    def from_derivation(
        self,
        identifier: str,
        derivation: Any,
    ) -> SemanticFrame:
        return self.from_upstream(
            identifier=identifier,
            label="Derivation Meaning Frame",
            upstream=derivation,
            role="derives-from",
            confidence=0.95,
            notes="Frame built from Derivation output.",
        )

    def from_samasa(
        self,
        identifier: str,
        samasa: Any,
    ) -> SemanticFrame:
        return self.from_upstream(
            identifier=identifier,
            label="Samasa Meaning Frame",
            upstream=samasa,
            role="compound",
            confidence=0.93,
            notes="Frame built from Samasa output.",
        )

    def from_grammar(
        self,
        identifier: str,
        grammar: Any,
    ) -> SemanticFrame:
        return self.from_upstream(
            identifier=identifier,
            label="Grammar Meaning Frame",
            upstream=grammar,
            role="grammatical",
            confidence=0.88,
            notes="Frame built from Grammar output.",
        )
