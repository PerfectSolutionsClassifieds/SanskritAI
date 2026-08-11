from __future__ import annotations

"""
Aṣṭādhyāyī 1.1.1

वृद्धिरादैच्

vṛddhir ādaic

Defines the technical grammatical designation (saṃjñā)
"Vṛddhi".

This is the very first sūtra of the Aṣṭādhyāyī.
"""

from dataclasses import replace

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)
from SanskritAI.domain.panini.paninian_rule_operation import (
    PaninianRuleOperation,
)
from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)
from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)
from SanskritAI.domain.panini.paninian_sutra import (
    PaninianSutra,
)
from SanskritAI.domain.panini.rules.samjna_rule import (
    SamjnaRule,
)


class Sutra111VrddhirAdaic(SamjnaRule):
    """
    Aṣṭādhyāyī 1.1.1

    वृद्धिरादैच्
    """

    def __init__(self) -> None:

        sutra = PaninianSutra(
            identifier="PANINI-1.1.1",
            sutra_number="1.1.1",
            sutra_text="वृद्धिरादैच्",
            transliteration="vṛddhir ādaic",
            translation="The vowels ā, ai and au are designated as Vṛddhi.",
            adhyaya=1,
            pada=1,
        )

        metadata = PaninianRuleMetadata(
            sutra=sutra,
            category=PaninianRuleCategory.SAMJNA,
            operation=PaninianRuleOperation.NONE,
            rule_type=PaninianRuleType.DEFINITION,
            priority=PaninianRulePriority.HIGHEST,
            source="Aṣṭādhyāyī",
            notes="Defines the grammatical technical term Vṛddhi.",
            tags=(
                "samjna",
                "vrddhi",
                "phonology",
            ),
        )

        super().__init__(
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Matching
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Always applicable.

        It merely establishes a technical designation.
        """
        return True

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context,
    ):
        """
        Registers the Vṛddhi designation.

        Current implementation simply records the
        designation in the derivation context.

        Future versions will integrate with the
        lexical designation repository.
        """

        if hasattr(context, "designations"):

            context.designations["VRDDHI"] = (
                "आ",
                "ऐ",
                "औ",
            )

        return (context,)
