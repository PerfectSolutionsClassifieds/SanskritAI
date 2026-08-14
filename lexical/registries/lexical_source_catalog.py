from __future__ import annotations

"""
SanskritAI
==========

Lexical Source Catalog

Provides a dedicated catalog for LexicalSource definitions.

The catalog manages the canonical sources from which lexical
knowledge is derived, such as:

- Monier-Williams
- Apte
- Amarakośa
- Śabdakalpadruma
- Vācaspatyam

The catalog is intentionally limited to source definitions.
Lexical records themselves remain the responsibility of
LexicalRegistry and future lexical repositories.

Version
-------
v0.3.0
"""

from collections.abc import Iterable, Iterator
from SanskritAI.lexical.models.lexical_source import LexicalSource


class LexicalSourceCatalog:
    """
    Registry-like catalog dedicated to LexicalSource objects.
    """

    def __init__(
        self,
        sources: Iterable[LexicalSource] | None = None,
    ) -> None:
        self._sources: dict[str, LexicalSource] = {}
        if sources is not None:
            self.register_many(sources)

    # =========================================================
    # Registration
    # =========================================================

    def register(self, source: LexicalSource) -> LexicalSource:
        """
        Register a lexical source.

        Raises
        ------
        TypeError
            If source is not a LexicalSource.
        ValueError
            If the identifier is empty or already registered.
        """
        if not isinstance(source, LexicalSource):
            raise TypeError(
                "source must be a LexicalSource."
            )
        identifier = self._normalize_identifier(source.identifier)
        if not identifier:
            raise ValueError(
                "source identifier must not be empty."
            )
        if identifier in self._sources:
            raise ValueError(
                f"Lexical source already registered: {identifier}"
            )
        self._sources[identifier] = source
        return source

    def register_many(
        self,
        sources: Iterable[LexicalSource],
    ) -> None:
        """
        Register multiple lexical sources.
        """
        for source in sources:
            self.register(source)

    # =========================================================
    # Lookup
    # =========================================================

    def get(
        self,
        identifier: str,
    ) -> LexicalSource | None:
        """
        Return a registered source or None.
        """
        key = self._normalize_identifier(identifier)
        return self._sources.get(key)

    def require(
        self,
        identifier: str,
    ) -> LexicalSource:
        """
        Return a registered source.

        Raises
        ------
        KeyError
            If the source is not registered.
        """
        key = self._normalize_identifier(identifier)
        source = self._sources.get(key)
        if source is None:
            raise KeyError(
                f"Unknown lexical source: {key}"
            )
        return source

    def exists(self, identifier: str) -> bool:
        """
        Return True when the identifier is registered.
        """
        return self._normalize_identifier(identifier) in self._sources

    # =========================================================
    # Removal
    # =========================================================

    def remove(self, identifier: str) -> LexicalSource:
        """
        Remove and return a registered source.

        Raises
        ------
        KeyError
            If the source is not registered.
        """
        key = self._normalize_identifier(identifier)
        try:
            return self._sources.pop(key)
        except KeyError:
            raise KeyError(
                f"Unknown lexical source: {key}"
            ) from None

    def clear(self) -> None:
        """
        Remove all registered sources.
        """
        self._sources.clear()

    # =========================================================
    # Projection
    # =========================================================

    @property
    def identifiers(self) -> tuple[str, ...]:
        """
        Return registered source identifiers in registration order.
        """
        return tuple(self._sources)

    @property
    def sources(self) -> tuple[LexicalSource, ...]:
        """
        Return registered sources in registration order.
        """
        return tuple(self._sources.values())

    @property
    def count(self) -> int:
        """
        Number of registered lexical sources.
        """
        return len(self._sources)

    def __contains__(self, identifier: object) -> bool:
        """
        Support ``identifier in catalog``.
        """
        if not isinstance(identifier, str):
            return False
        return self.exists(identifier)

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[LexicalSource]:
        return iter(self._sources.values())

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _normalize_identifier(identifier: str) -> str:
        """
        Normalize a source identifier for catalog lookup.
        """
        if not isinstance(identifier, str):
            raise TypeError(
                "identifier must be a string."
            )
        return identifier.strip()
