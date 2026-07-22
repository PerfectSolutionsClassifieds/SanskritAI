
from __future__ import annotations

"""
SanskritAI
==========

Canonical Work Definition Domain Model

This module defines the primary domain object representing a
canonical Sanskrit work.

A WorkDefinition is the central identity for a literary work,
independent of:

    • repository
    • edition
    • publication
    • filename
    • encoding
    • script
    • transliteration

Examples
--------
Canonical Works

    srimad_bhagavatam
    shiva_purana
    mahabharata
    ramayana
    amarakosha
    vacaspatyam

Each WorkDefinition may have dozens (or eventually hundreds) of
aliases originating from various repositories, OCR systems,
transliterations, or Unicode scripts.

Version
-------
v0.5.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.acquisition.metadata.models.work_alias import (
    WorkAlias,
)


@dataclass(slots=True)
class WorkDefinition:
    """
    Represents one canonical Sanskrit work.
    """

    #
    # Primary Identity
    #

    identifier: str

    title: str

    #
    # Alternate names
    #

    aliases: list[WorkAlias] = field(
        default_factory=list,
    )

    #
    # Optional metadata
    #

    corpus_type: str | None = None

    language: str = "sanskrit"

    script: str | None = None

    description: str | None = None

    author: str | None = None

    period: str | None = None

    repository: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Alias Operations
    # ---------------------------------------------------------

    def add_alias(
        self,
        alias: WorkAlias,
    ) -> None:
        """
        Add a new alias if it does not already exist.
        """

        if alias not in self.aliases:

            self.aliases.append(alias)

    # ---------------------------------------------------------

    def remove_alias(
        self,
        value: str,
    ) -> bool:
        """
        Remove an alias.

        Returns
        -------
        bool
            True if removed.
        """

        for alias in self.aliases:

            if alias.value == value:

                self.aliases.remove(alias)

                return True

        return False

    # ---------------------------------------------------------

    def find_alias(
        self,
        text: str,
    ) -> WorkAlias | None:
        """
        Returns the matching alias, if any.
        """

        for alias in self.aliases:

            if alias.matches(text):

                return alias

        return None

    # ---------------------------------------------------------

    def matches(
        self,
        text: str,
    ) -> bool:
        """
        True if any alias matches.
        """

        return self.find_alias(text) is not None

    # ---------------------------------------------------------

    @property
    def preferred_alias(
        self,
    ) -> WorkAlias | None:
        """
        Returns the preferred alias.

        Falls back to the first alias.
        """

        for alias in self.aliases:

            if alias.is_preferred:

                return alias

        if self.aliases:

            return self.aliases[0]

        return None

    # ---------------------------------------------------------

    @property
    def alias_count(
        self,
    ) -> int:

        return len(self.aliases)

    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize for JSON/YAML.
        """

        return {

            "identifier": self.identifier,

            "title": self.title,

            "aliases": [

                {

                    "value": alias.value,

                    "language": alias.language,

                    "script": alias.script,

                    "is_preferred": alias.is_preferred,

                    "source": alias.source,

                }

                for alias in self.aliases

            ],

            "corpus_type": self.corpus_type,

            "language": self.language,

            "script": self.script,

            "description": self.description,

            "author": self.author,

            "period": self.period,

            "repository": self.repository,

            "metadata": self.metadata,

        }

    # ---------------------------------------------------------

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "WorkDefinition":
        """
        Construct from JSON/YAML.
        """

        aliases = [

            WorkAlias(

                value=item["value"],

                language=item.get("language"),

                script=item.get("script"),

                is_preferred=item.get(
                    "is_preferred",
                    False,
                ),

                source=item.get("source"),

            )

            for item in data.get(
                "aliases",
                [],
            )

        ]

        return cls(

            identifier=data["identifier"],

            title=data["title"],

            aliases=aliases,

            corpus_type=data.get(
                "corpus_type",
            ),

            language=data.get(
                "language",
                "sanskrit",
            ),

            script=data.get(
                "script",
            ),

            description=data.get(
                "description",
            ),

            author=data.get(
                "author",
            ),

            period=data.get(
                "period",
            ),

            repository=data.get(
                "repository",
            ),

            metadata=data.get(
                "metadata",
                {},
            ),

        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        text: str,
    ) -> bool:

        return self.matches(text)

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self.aliases)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "WorkDefinition("
            f"identifier={self.identifier!r}, "
            f"title={self.title!r}, "
            f"aliases={len(self.aliases)}, "
            f"corpus_type={self.corpus_type!r})"
        )
