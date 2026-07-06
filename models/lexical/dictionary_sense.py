"""
SanskritAI
==========

Module:
    models.lexical.dictionary_sense

Description:
    Represents one semantic sense (meaning) within a dictionary entry.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DictionarySense:
    """
    One semantic meaning within a dictionary entry.

    A single DictionaryEntry may contain multiple semantic senses.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    sense_id: str

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    definition: str

    language: str = "en"

    examples: list[str] = field(default_factory=list)

    notes: str = ""

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Validate and normalize the object.
        """

        self.sense_id = self.sense_id.strip()
        self.definition = self.definition.strip()
        self.language = self.language.strip()
        self.notes = self.notes.strip()

        if not self.sense_id:
            raise ValueError("sense_id cannot be empty.")

        if not self.definition:
            raise ValueError("definition cannot be empty.")

    # ---------------------------------------------------------
    # Operations
    # ---------------------------------------------------------

    def add_example(
        self,
        example: str,
    ) -> None:
        """
        Add an example sentence.

        Duplicate examples are ignored.
        """

        example = example.strip()

        if example and example not in self.examples:
            self.examples.append(example)

    # ---------------------------------------------------------
    # Computed Properties
    # ---------------------------------------------------------

    @property
    def example_count(self) -> int:
        """
        Number of example sentences.
        """

        return len(self.examples)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize to a JSON-compatible dictionary.
        """

        return {
            "sense_id": self.sense_id,
            "definition": self.definition,
            "language": self.language,
            "examples": list(self.examples),
            "notes": self.notes,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.definition

    def __repr__(self) -> str:
        return (
            "DictionarySense("
            f"id='{self.sense_id}', "
            f"language='{self.language}', "
            f"examples={self.example_count})"
        )
