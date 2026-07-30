from __future__ import annotations

"""
SanskritAI
==========

Nominal Morphological Rule

Rule-based morphological analysis for Sanskrit nominal forms.

This rule attempts to recognize nominal patterns and produce
a typed MorphologicalAnalysis with nominal grammatical
categories.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.linga import Linga
from SanskritAI.domain.morphology.morphological_analysis import (
    MorphologicalAnalysis,
)
from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)
from SanskritAI.domain.morphology.morphological_features import (
    MorphologicalFeatures,
)
from SanskritAI.domain.morphology.morphological_rule import (
    MorphologicalRule,
)
from SanskritAI.domain.morphology.vacana import Vacana
from SanskritAI.domain.morphology.vibhakti import Vibhakti


class NominalMorphologicalRule(
    MorphologicalRule,
):
    """
    Heuristic nominal morphology rule.

    This is an initial rule intended to recognize common
    nominal endings and emit a nominal analysis candidate.
    """

    _COMMON_NOMINAL_SUFFIXES: tuple[str, ...] = (
        "am",
        "ā",
        "i",
        "ī",
        "u",
        "ū",
        "e",
        "o",
        "ena",
        "āya",
        "āt",
        "ād",
        "asya",
        "eṣu",
        "aiḥ",
        "ebhiḥ",
        "bhyaḥ",
        "tām",
        "yam",
        "ena",
    )

    @property
    def display_name(self) -> str:
        return "Nominal Morphological Rule"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Heuristic rule for nominal Sanskrit word forms."
        )

    def applies_to(
        self,
        word_form: WordForm,
    ) -> bool:
        text = word_form.text.strip()
        if not text:
            return False

        return text.endswith(self._COMMON_NOMINAL_SUFFIXES)

    def _guess_stem(
        self,
        text: str,
    ) -> str:
        for suffix in sorted(
            self._COMMON_NOMINAL_SUFFIXES,
            key=len,
            reverse=True,
        ):
            if text.endswith(suffix):
                stem = text[: -len(suffix)]
                return stem or text

        return text

    def apply(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        if not self.applies_to(word_form):
            return MorphologicalAnalysisCollection()

        stem = self._guess_stem(word_form.text)

        features = MorphologicalFeatures(
            stem=stem,
            root=word_form.lemma.text,
            vibhakti=Vibhakti(),
            vacana=Vacana(),
            linga=Linga(),
            description=(
                "Nominal form detected by heuristic suffix analysis."
            ),
        )

        analysis = MorphologicalAnalysis(
            identifier=f"{word_form.identifier}:nominal",
            word_form=word_form,
            features=features,
            analyzer=self.display_name,
            confidence=0.55,
            notes=(
                "Heuristic nominal analysis candidate. "
                "Refine with dictionary and grammar rules."
            ),
        )

        return MorphologicalAnalysisCollection(
            analyses=(analysis,),
        )
