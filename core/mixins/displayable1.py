from __future__ import annotations

"""
SanskritAI
==========

Displayable Mixin

Defines a lightweight semantic contract for objects that can be
presented in a human-readable form.

This mixin intentionally avoids any dependency on user
interfaces, formatting libraries, or presentation frameworks.

Typical users include:

- Language
- Script
- Lexeme
- Synset
- DictionaryEntry
- Corpus objects
- Knowledge objects

Architecture
------------

Displayable
      │
      ├── Language
      ├── Script
      ├── Lexeme
      ├── Synset
      └── DictionaryEntry

Version
-------
v0.6.0
"""


class Displayable:
    """
    Semantic mixin for displayable objects.
    """

    @property
    def display_name(self) -> str:
        """
        Short human-readable name.

        The default implementation delegates to ``str(self)``.
        """
        return str(self)

    @property
    def display_text(self) -> str:
        """
        Human-readable textual representation.

        Subclasses may override this for richer descriptions.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Optional longer description.

        Defaults to an empty string.
        """
        return ""

    def to_display_string(self) -> str:
        """
        Returns the canonical display representation.
        """
        return self.display_text
