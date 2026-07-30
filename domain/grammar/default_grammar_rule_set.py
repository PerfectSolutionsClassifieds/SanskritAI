from __future__ import annotations

"""
SanskritAI
==========

Default Grammar Rule Set

Provides the canonical reusable GrammarRuleSet for the Grammar
Kernel.

Future grammar analyzers can import this helper instead of
repeating the same kartā and karma rule wiring.

Version
-------
v1.0.0
"""

from SanskritAI.domain.grammar.grammar_rule_set import GrammarRuleSet
from SanskritAI.domain.grammar.karma_grammar_rule import KarmaGrammarRule
from SanskritAI.domain.grammar.karta_grammar_rule import KartaGrammarRule


def default_grammar_rule_set() -> GrammarRuleSet:
    """
    Returns the canonical rule bundle for Sanskrit grammar.
    """
    return GrammarRuleSet(
        rules=(
            KartaGrammarRule(),
            KarmaGrammarRule(),
        ),
    )
