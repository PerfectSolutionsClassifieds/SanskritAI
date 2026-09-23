from __future__ import annotations

"""
SanskritAI
==========

Aṣṭādhyāyī 1.1.1

वृद्धिरादैच्

vṛddhir ādaic

Defines the technical grammatical designation (saṃjñā)
"Vṛddhi".

The canonical sūtra is registered automatically when
this module is imported by PaninianSutraLoader.
"""

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

from SanskritAI.domain.panini.paninian_sutra_registration import (
    register_paninian_sutra,
)

from SanskritAI.domain.panini.rules.samjna_rule import (
    SamjnaRule,
)


@register_paninian_sutra(
    "1.1.1",
)
class Sutra111VrddhirAdaic(
    SamjnaRule,
):
    """
    Aṣṭādhyāyī 1.1.1

    वृद्धिरादैच्

    Vṛddhi designation:
        आ
        ऐ
        औ
    """

    def __init__(
        self,
    ) -> None:

        sutra = PaninianSutra(
            identifier="PANINI-1.1.1",
            sutra_number="1.1.1",
            sutra_text="वृद्धिरादैच्",
            transliteration="vṛddhir ādaic",
            translation=(
                "The vowels ā, ai and au "
                "are designated as Vṛddhi."
            ),
            adhyaya=1,
            pada=1,
            source="Aṣṭādhyāyī",
        )

        metadata = PaninianRuleMetadata(
            sutra=sutra,
            category=PaninianRuleCategory.SAMJNA,
            operation=PaninianRuleOperation.NONE,
            rule_type=PaninianRuleType.DEFINITION,
            priority=PaninianRulePriority.HIGHEST,
            source="Aṣṭādhyāyī",
            notes=(
                "Defines the grammatical "
                "technical term Vṛddhi."
            ),
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
        1.1.1 is a Saṃjñā rule establishing
        the Vṛddhi technical designation.

        The current kernel allows the rule to
        participate in every derivation.
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
        Records the Vṛddhi designation.

        The current kernel keeps this operation
        deliberately lightweight. Future versions
        may connect this designation to the canonical
        technical-term repository.
        """

        if hasattr(
            context,
            "designations",
        ):
            context.designations["VRDDHI"] = (
                "आ",
                "ऐ",
                "औ",
            )

        return (
            context,
        )
