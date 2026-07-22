from __future__ import annotations

"""
SanskritAI
==========

Lexical Registry

Central registry for lexical objects.

The registry stores and retrieves lexical domain objects by
their identifiers while remaining agnostic to their concrete
types.

Supported objects include:

- Lexeme
- DictionaryEntry
- DictionarySense
- LexicalRelation

Future lexical object types may also be registered without
modifying this implementation.

Version
-------
v0.3.0
"""

from typing import Iterable

from SanskritAI.core.registries.base_registry import (
    BaseRegistry,
)

from SanskritAI.lexical.models.base_lexical_node import (
    BaseLexicalNode,
)


class LexicalRegistry(
    BaseRegistry[
        str,
        BaseLexicalNode,
    ]
):
    """
    Registry for lexical objects.
    """

    def register_many(
        self,
        objects: Iterable[BaseLexicalNode],
    ) -> None:
        """
        Register multiple lexical objects.
        """

        for obj in objects:
            self.register(obj)

    # ---------------------------------------------------------

    def lexemes(self):
        """
        Iterate over registered Lexeme objects.
        """

        from SanskritAI.lexical.models.lexeme import Lexeme

        for obj in self.values():
            if isinstance(obj, Lexeme):
                yield obj

    # ---------------------------------------------------------

    def dictionary_entries(self):
        """
        Iterate over registered DictionaryEntry objects.
        """

        from SanskritAI.lexical.models.dictionary_entry import (
            DictionaryEntry,
        )

        for obj in self.values():
            if isinstance(obj, DictionaryEntry):
                yield obj

    # ---------------------------------------------------------

    def dictionary_senses(self):
        """
        Iterate over registered DictionarySense objects.
        """

        from SanskritAI.lexical.models.dictionary_sense import (
            DictionarySense,
        )

        for obj in self.values():
            if isinstance(obj, DictionarySense):
                yield obj

    # ---------------------------------------------------------

    def lexical_relations(self):
        """
        Iterate over registered LexicalRelation objects.
        """

        from SanskritAI.lexical.models.lexical_relation import (
            LexicalRelation,
        )

        for obj in self.values():
            if isinstance(obj, LexicalRelation):
                yield obj
