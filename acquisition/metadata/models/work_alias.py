from __future__ import annotations

"""
SanskritAI
==========

Work Alias Domain Model

Represents one alias (alternate title) for a canonical Sanskrit work.

Examples
--------
Canonical Work
    srimad_bhagavatam

Aliases
    Bhagavatam
    Bhagavata Purana
    Śrīmad Bhāgavatam
    भागवत
    भागवतपुराण

Version
-------
v0.5.0
"""

from dataclasses import dataclass
import unicodedata
import re


@dataclass(frozen=True, slots=True, order=True)
class WorkAlias:
    """
    Represents a single alias for a Sanskrit work.
    """

    value: str

    language: str | None = None

    script: str | None = None

    is_preferred: bool = False

    source: str | None = None

    # ---------------------------------------------------------

    @property
    def normalized(self) -> str:
        """
        Normalized value used for matching.
        """

        text = unicodedata.normalize(
            "NFKC",
            self.value,
        )

        text = text.lower()

        text = re.sub(
            r"[_\-]+",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # ---------------------------------------------------------

    def matches(
        self,
        text: str,
    ) -> bool:
        """
        Returns True if this alias occurs within the supplied text.
        """

        searchable = unicodedata.normalize(
            "NFKC",
            text,
        )

        searchable = searchable.lower()

        searchable = re.sub(
            r"[_\-]+",
            " ",
            searchable,
        )

        searchable = re.sub(
            r"\s+",
            " ",
            searchable,
        )

        searchable = searchable.strip()

        return self.normalized in searchable

    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.value

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"WorkAlias("
            f"value={self.value!r}, "
            f"language={self.language!r}, "
            f"script={self.script!r})"
        )
