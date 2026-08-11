
from __future__ import annotations

"""
SanskritAI
==========

Aṣṭādhyāyī 1.1.1

वृद्धिरादैच्

vṛddhir ādaic

Defines the technical grammatical designation
"Vṛddhi".

The sūtra is classified as:

    Category:
        Saṃjñā

    Operation:
        None

The designated vowels are:

    आ
    ऐ
    औ

Version
-------
v1.1.0
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

    vṛddhir ādaic

    "The vowels ā, ai and au are designated
    as Vṛddhi."
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
                "The vowels ā, ai and au are "
                "designated as Vṛddhi."
            ),
            adhyaya=1,
            pada=1,
            source="Aṣṭādhyāyī",
        )

        metadata = PaninianRuleMetadata(
            sutra=sutra,
            category=PaninianRuleCategory.SAMJNA,
            operation=PaninianRuleOperation.NONE,
            # rule_type=PaninianRuleType.DEFINITION,
            rule_type=PaninianRuleType.ANNOTATION,
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
        Sūtra 1.1.1 is a Saṃjñā rule.

        It establishes the Vṛddhi designation and therefore
        participates in the current minimal execution kernel
        whenever the rule matcher evaluates executable rules.
        """

        return True

    def validate(
        self,
        context,
    ) -> bool:
        """
        The canonical rule currently requires no additional
        contextual validation.
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
        Register the Vṛddhi designation in the derivation
        context.

        The current kernel intentionally performs only the
        semantic designation. More advanced lexical and
        phonological integration can be added later.
        """

        if hasattr(
            context,
            "designations",
        ):
            context.designations[
                "VRDDHI"
            ] = (
                "आ",
                "ऐ",
                "औ",
            )

        return (
            context,
        )
