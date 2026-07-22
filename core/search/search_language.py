from __future__ import annotations

"""
SanskritAI
==========

Search Language

Defines the canonical language targets supported by the
SanskritAI Search Kernel.

SearchLanguage specifies the language (or language policy)
against which a search query should be executed.

Unlike Language enums used elsewhere in the system,
SearchLanguage represents search behaviour rather than
linguistic metadata.

Typical usages include:

- Search only Sanskrit
- Search only Telugu
- Search only English
- Multilingual search
- Auto language detection

Architecture
------------

SearchLanguage
        │
        ▼
SearchQuery

Version
-------
v0.6.0
"""

from enum import Enum


class SearchLanguage(str, Enum):
    """
    Canonical search languages.
    """

    # ---------------------------------------------------------
    # Automatic detection
    # ---------------------------------------------------------

    AUTO = "auto"

    # ---------------------------------------------------------
    # Classical Sanskrit
    # ---------------------------------------------------------

    SANSKRIT = "sanskrit"

    # ---------------------------------------------------------
    # Indian languages
    # ---------------------------------------------------------

    TELUGU = "telugu"

    HINDI = "hindi"

    TAMIL = "tamil"

    KANNADA = "kannada"

    MALAYALAM = "malayalam"

    MARATHI = "marathi"

    GUJARATI = "gujarati"

    BENGALI = "bengali"

    ODIA = "odia"

    PUNJABI = "punjabi"

    # ---------------------------------------------------------
    # International
    # ---------------------------------------------------------

    ENGLISH = "english"

    # ---------------------------------------------------------
    # Policies
    # ---------------------------------------------------------

    MULTILINGUAL = "multilingual"

    ALL = "all"

    @property
    def is_policy(self) -> bool:
        """
        Returns True if this value represents a search policy
        rather than a specific language.
        """
        return self in {
            SearchLanguage.AUTO,
            SearchLanguage.MULTILINGUAL,
            SearchLanguage.ALL,
        }

    @property
    def is_indic(self) -> bool:
        """
        Returns True if this language belongs to the Indic
        language family.
        """
        return self in {
            SearchLanguage.SANSKRIT,
            SearchLanguage.TELUGU,
            SearchLanguage.HINDI,
            SearchLanguage.TAMIL,
            SearchLanguage.KANNADA,
            SearchLanguage.MALAYALAM,
            SearchLanguage.MARATHI,
            SearchLanguage.GUJARATI,
            SearchLanguage.BENGALI,
            SearchLanguage.ODIA,
            SearchLanguage.PUNJABI,
        }

    @property
    def is_single_language(self) -> bool:
        """
        Returns True if this represents one concrete language.
        """
        return not self.is_policy
