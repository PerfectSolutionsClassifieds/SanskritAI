from __future__ import annotations

"""
SanskritAI
==========

Displayable Mixin

Provides lightweight display semantics for immutable domain
objects.

This mixin intentionally contains no UI, formatting, rendering,
or serialization logic. It merely defines a canonical,
human-readable representation that higher-level presentation
layers may consume.

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
    Lightweight semantic mixin for displayable objects.
    """

    __slots__ = ()

    @property
    def is_displayable(self) -> bool:
        """
        Indicates that this object supports the Displayable API.
        """
        return True

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
        Canonical human-readable representation.

        Subclasses may override this to provide richer text.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Optional extended description.

        Defaults to an empty string.
        """
        return ""

    def to_display_string(self) -> str:
        """
        Returns the canonical display representation.

        This convenience method delegates to ``display_text`` and
        exists for APIs that prefer an explicit conversion method.
        """
        return self.display_text
