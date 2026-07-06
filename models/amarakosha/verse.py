"""
SanskritAI
==========

Module:
    models.amarakosha.verse

Description
-----------
Represents one canonical verse (śloka) of the Amarakośa.

This class is intentionally lightweight. It models only the textual
structure of the Amarakośa and contains no parsing, lexical analysis,
or repository logic.

Future importer stages will enrich Verse objects with tokenization,
Lexeme mappings, grammatical analyses, and semantic annotations.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Verse:
    """
    Represents one Amarakośa verse.

    Examples
    --------

    अमरकोश १.१.१

        स्वर्गो द्यौर्दिव् ...

    Notes
    -----
    The verse stores only canonical textual information.

    Lexical objects are generated later by the importer.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    verse_id: str

    verse_number: int

    # ---------------------------------------------------------
    # Text
    # ---------------------------------------------------------

    text: str

    transliteration: str = ""

    translation: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    commentary: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # Future Extensions
    # ---------------------------------------------------------

    tokens: list[str] = field(default_factory=list)

    lexeme_ids: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        self.verse_id = self.verse_id.strip()

        self.text = self.text.strip()

        if not self.verse_id:
            raise ValueError(
                "verse_id cannot be empty."
            )

        if self.verse_number <= 0:
            raise ValueError(
                "verse_number must be positive."
            )

        if not self.text:
            raise ValueError(
                "text cannot be empty."
            )

    # ---------------------------------------------------------
    # Token Operations
    # ---------------------------------------------------------

    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Add one token.

        Duplicate tokens are ignored.
        """

        token = token.strip()

        if token and token not in self.tokens:
            self.tokens.append(token)

    def clear_tokens(self) -> None:

        self.tokens.clear()

    @property
    def token_count(self) -> int:

        return len(self.tokens)

    # ---------------------------------------------------------
    # Lexeme Operations
    # ---------------------------------------------------------

    def add_lexeme(
        self,
        lexeme_id: str,
    ) -> None:
        """
        Associate a canonical Lexeme with this verse.

        Duplicate IDs are ignored.
        """

        lexeme_id = lexeme_id.strip()

        if lexeme_id and lexeme_id not in self.lexeme_ids:
            self.lexeme_ids.append(lexeme_id)

    def clear_lexemes(self) -> None:

        self.lexeme_ids.clear()

    @property
    def lexeme_count(self) -> int:

        return len(self.lexeme_ids)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "verse_id": self.verse_id,

            "verse_number": self.verse_number,

            "text": self.text,

            "transliteration": self.transliteration,

            "translation": self.translation,

            "commentary": self.commentary,

            "notes": self.notes,

            "token_count": self.token_count,

            "lexeme_count": self.lexeme_count,

            "tokens": list(self.tokens),

            "lexeme_ids": list(self.lexeme_ids),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.text

    def __repr__(self) -> str:

        return (
            "Verse("
            f"id='{self.verse_id}', "
            f"number={self.verse_number}, "
            f"tokens={self.token_count}, "
            f"lexemes={self.lexeme_count})"
        )
