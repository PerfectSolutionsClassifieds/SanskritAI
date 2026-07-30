from __future__ import annotations

"""
SanskritAI
==========

Pratyaya to Derivation Bridge

Converts richer Pratyaya repository matches into derivation
candidate payloads in a systematic way.

This bridge is especially useful for Kṛt and Taddhita affixes,
where the Pratyaya knowledge layer can be translated into
derivation-ready candidate data before the main derivation
strategy ranks and normalizes outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any, Iterable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.pratyaya.pratyaya_analysis import PratyayaAnalysis
from SanskritAI.domain.pratyaya.pratyaya_analysis_collection import (
    PratyayaAnalysisCollection,
)
from SanskritAI.domain.pratyaya.pratyaya_factory import Pratyaya
from SanskritAI.domain.pratyaya.pratyaya_factory import PratyayaCollection
from SanskritAI.domain.pratyaya.pratyaya_result import PratyayaResult


@dataclass(frozen=True, slots=True)
class DerivationCandidate(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One derivation-ready candidate produced from a Dhatu and a
    Pratyaya match.
    """

    identifier: str

    dhatu: Dhatu

    pratyaya: Pratyaya

    surface_form: str

    pada: str = ""

    pattern: str = ""

    confidence: float = 1.0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.surface_form

    @property
    def display_text(self) -> str:
        if self.pada:
            return f"{self.surface_form} ({self.pada})"
        return self.surface_form

    @property
    def display_description(self) -> str:
        return self.notes or self.pattern

    @property
    def has_pada(self) -> bool:
        return bool(self.pada)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    @property
    def has_pattern(self) -> bool:
        return bool(self.pattern)

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text


@dataclass(frozen=True, slots=True)
class DerivationCandidateCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of derivation candidates.
    """

    candidates: tuple[DerivationCandidate, ...] = ()

    @property
    def display_name(self) -> str:
        return "Derivation Candidates"

    @property
    def display_text(self) -> str:
        return f"{len(self.candidates)} candidates"

    @property
    def display_description(self) -> str:
        return "Immutable collection of derivation candidates."

    @property
    def count(self) -> int:
        return len(self.candidates)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> DerivationCandidate | None:
        if self.is_empty:
            return None
        return self.candidates[0]

    def add(
        self,
        candidate: DerivationCandidate,
    ) -> "DerivationCandidateCollection":
        return DerivationCandidateCollection(
            candidates=self.candidates + (candidate,)
        )

    def extend(
        self,
        other: "DerivationCandidateCollection",
    ) -> "DerivationCandidateCollection":
        return DerivationCandidateCollection(
            candidates=self.candidates + other.candidates
        )

    def __iter__(self):
        return iter(self.candidates)

    def __len__(self) -> int:
        return len(self.candidates)

    def __getitem__(self, index: int) -> DerivationCandidate:
        return self.candidates[index]

    def __str__(self) -> str:
        return self.display_text


class PratyayaToDerivationBridge:
    """
    Converts Pratyaya repository matches into derivation
    candidate payloads.

    The bridge is intentionally conservative:
    - Kṛt affixes receive canonical derivational templates.
    - Taddhita affixes receive nominal/agentive templates.
    - Any other affix still produces a valid derivation-ready
      payload, but with a generic template label.

    The bridge does not perform the final derivation itself.
    It prepares rich candidate data for the derivation kernel.
    """

    _KRIT_TEMPLATES: dict[str, tuple[str, str]] = {
        "क्त": ("bhū + kta", "root + past participle"),
        "क्त्वा": ("gam + ktvā", "root + absolutive"),
        "ल्यप्": ("kṛ + lyap", "root + absolutive variant"),
        "तुमुन्": ("root + tumun", "infinitive template"),
        "शतृ": ("root + śatṛ", "present active participle"),
        "शानच्": ("root + śānac", "present middle participle"),
        "अनीय": ("root + anīya", "desiderative/passive adjective"),
    }

    _TADDHITA_TEMPLATES: dict[str, tuple[str, str]] = {
        "ण्वुल्": ("base + ṇvul", "agentive derivation"),
    }

    @property
    def display_name(self) -> str:
        return "Pratyaya to Derivation Bridge"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Bridges Pratyaya matches into derivation-ready "
            "candidate payloads."
        )

    def _normalize_analysis(
        self,
        item: Any,
    ) -> PratyayaAnalysis | None:
        if isinstance(item, PratyayaAnalysis):
            return item

        if isinstance(item, dict):
            pratyaya = str(item.get("pratyaya", "")).strip()
            if not pratyaya:
                return None

            return PratyayaAnalysis(
                identifier=str(item.get("identifier", pratyaya)),
                pratyaya=pratyaya,
                transliteration=str(item.get("transliteration", "")).strip(),
                meaning=str(item.get("meaning", "")).strip(),
                confidence=float(item.get("confidence", 1.0)),
                matched_rule=str(item.get("matched_rule", "")).strip(),
                notes=str(item.get("notes", "")).strip(),
            )

        return None

    def _analysis_iter(
        self,
        pratyaya_source: (
            PratyayaResult
            | PratyayaAnalysisCollection
            | PratyayaCollection
            | Iterable[Any]
        ),
    ) -> Iterable[PratyayaAnalysis]:
        if isinstance(pratyaya_source, PratyayaResult):
            return pratyaya_source.analyses

        if isinstance(pratyaya_source, PratyayaAnalysisCollection):
            return pratyaya_source

        if isinstance(pratyaya_source, PratyayaCollection):
            analyses: list[PratyayaAnalysis] = []
            for item in pratyaya_source:
                analyses.append(
                    PratyayaAnalysis(
                        identifier=item.identifier,
                        pratyaya=item.pratyaya,
                        transliteration=item.transliteration,
                        meaning=item.meaning,
                        confidence=1.0,
                        matched_rule="repository",
                        notes=item.category or item.notes,
                    )
                )
            return tuple(analyses)

        normalized: list[PratyayaAnalysis] = []
        for item in pratyaya_source:
            analysis = self._normalize_analysis(item)
            if analysis is not None:
                normalized.append(analysis)
        return tuple(normalized)

    def _pattern_for(
        self,
        pratyaya: PratyayaAnalysis,
    ) -> tuple[str, str]:
        symbol = pratyaya.pratyaya.strip()

        if symbol in self._KRIT_TEMPLATES:
            return self._KRIT_TEMPLATES[symbol]

        if symbol in self._TADDHITA_TEMPLATES:
            return self._TADDHITA_TEMPLATES[symbol]

        category = pratyaya.meaning.strip().lower()
        if "participle" in category or "absolutive" in category or "infinitive" in category:
            return (f"{pratyaya.pratyaya} template", "canonical kṛt template")

        if "agentive" in category or "taddhita" in pratyaya.display_description.lower():
            return (f"{pratyaya.pratyaya} template", "canonical taddhita template")

        return (f"{pratyaya.pratyaya} template", "generic derivation template")

    def bridge(
        self,
        dhatu: Dhatu,
        pratyaya_source: (
            PratyayaResult
            | PratyayaAnalysisCollection
            | PratyayaCollection
            | Iterable[Any]
        ),
        *,
        identifier_prefix: str = "bridge",
    ) -> DerivationCandidateCollection:
        """
        Converts pratyaya matches into derivation-ready
        candidate objects for one Dhatu.
        """
        candidates = DerivationCandidateCollection()

        for index, analysis in enumerate(
            self._analysis_iter(pratyaya_source),
            start=1,
        ):
            try:
                pratyaya_obj = Pratyaya(
                    identifier=analysis.identifier,
                    pratyaya=analysis.pratyaya,
                    transliteration=analysis.transliteration,
                    meaning=analysis.meaning,
                    category="",
                    notes=analysis.notes,
                )
            except Exception:
                # Fallback for environments where a strict Pratyaya
                # object cannot be instantiated from partial analysis.
                continue

            template_name, template_reason = self._pattern_for(analysis)

            surface_form = f"{dhatu.root}{pratyaya_obj.pratyaya}"
            pada = surface_form

            candidates = candidates.add(
                DerivationCandidate(
                    identifier=f"{identifier_prefix}:{dhatu.identifier}:{index}",
                    dhatu=dhatu,
                    pratyaya=pratyaya_obj,
                    surface_form=surface_form,
                    pada=pada,
                    pattern=template_name,
                    confidence=max(analysis.confidence, 0.75),
                    notes=template_reason,
                )
            )

        return candidates

    def to_payloads(
        self,
        dhatu: Dhatu,
        pratyaya_source: (
            PratyayaResult
            | PratyayaAnalysisCollection
            | PratyayaCollection
            | Iterable[Any]
        ),
    ) -> tuple[dict[str, Any], ...]:
        """
        Converts pratyaya matches into plain derivation payloads.
        Useful when the derivation strategy expects dictionaries.
        """
        candidates = self.bridge(dhatu, pratyaya_source)

        return tuple(
            {
                "type": "PratyayaBridgeCandidate",
                "surface": candidate.surface_form,
                "pada": candidate.pada,
                "dhatu": candidate.dhatu.root,
                "pratyaya": candidate.pratyaya.pratyaya,
                "confidence": candidate.confidence,
                "analysis": candidate.notes,
                "pattern": candidate.pattern,
            }
            for candidate in candidates
        )
