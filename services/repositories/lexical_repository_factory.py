"""
SanskritAI
==========

Module:
    services.repositories.lexical_repository_factory

Description
-----------
Factory responsible for creating LexicalRepository instances.

Analysis code should never instantiate repository implementations
directly. All repositories are obtained through this factory.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from typing import Type

from core.config import Config

from .lexical_repository_base import LexicalRepositoryBase
from .memory_lexical_repository import MemoryLexicalRepository


class LexicalRepositoryFactory:
    """
    Factory for creating LexicalRepository implementations.
    """

    DEFAULT_BACKEND = "memory"

    _registry: dict[
        str,
        Type[LexicalRepositoryBase],
    ] = {
        "memory": MemoryLexicalRepository,
    }

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        backend: str,
        repository_class: Type[LexicalRepositoryBase],
    ) -> None:
        """
        Register a repository implementation.
        """

        if not issubclass(
            repository_class,
            LexicalRepositoryBase,
        ):
            raise TypeError(
                "Repository must inherit "
                "LexicalRepositoryBase."
            )

        cls._registry[
            backend.lower()
        ] = repository_class

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    @classmethod
    def create(
        cls,
        backend: str | None = None,
    ) -> LexicalRepositoryBase:
        """
        Create a repository instance.
        """

        if backend is None:

            backend = getattr(
                Config,
                "LEXICAL_REPOSITORY",
                cls.DEFAULT_BACKEND,
            )

        backend = backend.lower()

        repository_class = cls._registry.get(
            backend
        )

        if repository_class is None:

            if backend in (
                "json",
                "postgres",
                "neo4j",
                "mongodb",
            ):
                raise NotImplementedError(
                    f"{backend} repository "
                    "has not yet been implemented."
                )

            raise ValueError(
                f"Unknown repository backend: "
                f"'{backend}'"
            )

        return repository_class()

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @classmethod
    def available_backends(
        cls,
    ) -> tuple[str, ...]:
        """
        Return all known backend names.
        """

        return tuple(
            sorted(cls._registry.keys())
        )

    @classmethod
    def is_supported(
        cls,
        backend: str,
    ) -> bool:
        """
        Return True if the backend name is recognized.
        """

        return backend.lower() in cls._registry

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "LexicalRepositoryFactory("
            f"backends={len(self._registry)})"
        )
