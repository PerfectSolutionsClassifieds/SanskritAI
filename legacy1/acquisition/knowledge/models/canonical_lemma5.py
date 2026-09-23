
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class CanonicalLemma:
    """
    Immutable canonical representation of a Sanskrit lemma.

    The lemma itself is the canonical identity. Compatibility aliases
    ``text`` and ``lemma_id`` intentionally resolve to the same value.
    """

    lemma: str
    transliteration: Optional[str] = None
    language: str = "sa"
    script: str = "Devanagari"
    dhatu: Optional[str] = None
    part_of_speech: Optional[str] = None
    lexical_category: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # =========================================================
    # Canonical / Compatibility Accessors
    # =========================================================

    @property
    def text(self) -> str:
        """
        Compatibility alias for the canonical lemma text.
        """
        return self.lemma

    @property
    def lemma_id(self) -> str:
        """
        Deterministic canonical identifier for the lemma.

        The current canonical identity model uses the lemma text itself
        as the stable identifier.
        """
        return self.lemma

    # =========================================================
    # Convenience
    # =========================================================

    @property
    def display_name(self) -> str:
        """
        Human-readable display name.
        """
        return self.lemma

    # =========================================================
    # Summary
    # =========================================================

    def summary(self) -> Dict[str, Any]:
        """
        Return the canonical compact representation of the lemma.
        """
        return {
            "lemma": self.lemma,
            "lemma_id": self.lemma_id,
            "text": self.text,
            "dhatu": self.dhatu,
            "part_of_speech": self.part_of_speech,
            "category": self.lexical_category,
        }

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(self) -> str:
        return f"CanonicalLemma({self.lemma})"
        
