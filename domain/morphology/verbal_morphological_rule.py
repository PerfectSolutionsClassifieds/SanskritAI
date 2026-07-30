from __future__ import annotations

"""
SanskritAI
==========

Verbal Morphological Rule

Rule-based morphological analysis for Sanskrit verbal forms.

This rule attempts to recognize common verbal endings and
produce a typed MorphologicalAnalysis with verbal grammatical
categories.

Version
-------
v1.0.0
"""

from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.lakara import Lakara
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
from SanskritAI.domain.morphology.pada import Pada
from SanskritAI.domain.morphology.prayoga import Prayoga
from SanskritAI.domain.morphology.purusha import Purusha


class VerbalMorphologicalRule(
    MorphologicalRule,
):
    """
    Heuristic verbal morphology rule.

    This is an initial rule intended to recognize common
    verbal endings and emit a verbal analysis candidate.
    """

    _COMMON_VERBAL_SUFFIXES: tuple[str, ...] = (
        "ti",
        "anti",
        "si",
        "mi",
        "taḥ",
        "tām",
        "yati",
        "yanti",
        "ate",
        "ante",
        "ate",
        "e",
        "vaḥ",
        "maḥ",
        "athaḥ",
        "atha",
        "masi",
        "tas",
        "tasthau",
        "yāmi",
        "gacchati",
        "dadāti",
        "yāti",
    )

    @property
    def display_name(self) -> str:
        return "Verbal Morphological Rule"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Heuristic rule for verbal Sanskrit word forms."
        )

    def applies_to(
        self,
        word_form: WordForm,
    ) -> bool:
        text = word_form.text.strip()
        if not text:
            return False

        return text.endswith(self._COMMON_VERBAL_SUFFIXES)

    def _guess_stem(
        self,
        text: str,
    ) -> str:
        for suffix in sorted(
            self._COMMON_VERBAL_SUFFIXES,
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
            purusha=Purusha(),
            lakara=Lakara(),
            pada=Pada(),
            prayoga=Prayoga(),
            description=(
                "Verbal form detected by heuristic suffix analysis."
            ),
        )

        analysis = MorphologicalAnalysis(
            identifier=f"{word_form.identifier}:verbal",
            word_form=word_form,
            features=features,
            analyzer=self.display_name,
            confidence=0.55,
            notes=(
                "Heuristic verbal analysis candidate. "
                "Refine with grammar, dhātu, and conjugation rules."
            ),
        )

        return MorphologicalAnalysisCollection(
            analyses=(analysis,),
        )
