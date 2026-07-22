
from __future__ import annotations

"""
SanskritAI
==========

Acquisition Manager

High-level orchestration layer for corpus acquisition.

Responsibilities
----------------
* Provider selection
* Repository management
* Resource discovery
* Resource acquisition
* Validation
* Normalization
* Metadata extraction
* Acquisition statistics

The AcquisitionManager is the primary entry point for the
entire acquisition subsystem.

Architecture
------------

                AcquisitionManager
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 ProviderRegistry  RepositoryRegistry  Validators
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                 AcquisitionResponse
                        │
                        ▼
                Normalization
                        │
                        ▼
               Metadata Extraction
                        │
                        ▼
                    Import Pipeline

Version
-------
v0.7.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.normalizers.composite_normalizer import (
    CompositeNormalizer,
)

from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)

from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)

from SanskritAI.acquisition.providers.base_provider import (
    BaseProvider,
)

from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)

from SanskritAI.acquisition.repositories.repository_registry import (
    RepositoryRegistry,
)

from SanskritAI.acquisition.validators.base_validator import (
    BaseValidator,
)


class AcquisitionManager:
    """
    Orchestrates the complete acquisition workflow.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(self) -> None:

        self._providers: dict[
            str,
            BaseProvider,
        ] = {}

        self._repositories = RepositoryRegistry()

        self._validators: list[
            BaseValidator
        ] = []

        self._normalizer: CompositeNormalizer | None = None

    # ---------------------------------------------------------
    # Provider Registration
    # ---------------------------------------------------------

    def register_provider(
        self,
        provider: BaseProvider,
        *,
        replace: bool = False,
    ) -> None:

        identifier = provider.identifier.lower()

        if (
            identifier in self._providers
            and not replace
        ):

            raise ValueError(
                f"Provider '{identifier}' already registered."
            )

        self._providers[identifier] = provider

    # ---------------------------------------------------------

    def provider(
        self,
        identifier: str,
    ) -> BaseProvider:

        identifier = identifier.lower()

        if identifier not in self._providers:

            raise KeyError(
                f"Unknown provider '{identifier}'."
            )

        return self._providers[identifier]

    # ---------------------------------------------------------
    # Repository Registration
    # ---------------------------------------------------------

    def register_repository(
        self,
        repository: BaseRepositoryClient,
        *,
        replace: bool = False,
    ) -> None:

        self._repositories.register(
            repository,
            replace=replace,
        )

    # ---------------------------------------------------------
    # Validators
    # ---------------------------------------------------------

    def register_validator(
        self,
        validator: BaseValidator,
    ) -> None:

        self._validators.append(
            validator
        )

    # ---------------------------------------------------------
    # Normalizer
    # ---------------------------------------------------------

    def set_normalizer(
        self,
        normalizer: CompositeNormalizer,
    ) -> None:

        self._normalizer = normalizer

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:

        provider = self.provider(
            request.source_identifier
        )

        return provider.discover(
            request
        )

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    def acquire(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:

        provider = self.provider(
            request.source_identifier
        )

        response = provider.acquire(
            request
        )

        if not response:

            return response

        self._validate_downloads(
            response.downloaded_files
        )

        self._normalize_downloads(
            response.downloaded_files
        )

        response.finish()

        return response

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_downloads(
        self,
        files: Iterable[Path],
    ) -> None:

        for validator in self._validators:

            for file in files:

                validator.validate(file)

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def _normalize_downloads(
        self,
        files: Iterable[Path],
    ) -> None:

        if self._normalizer is None:

            return

        for file in files:

            self._normalizer.normalize(
                file
            )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def repository_health(
        self,
    ) -> dict[str, bool]:

        return self._repositories.health_report()

    # ---------------------------------------------------------

    @property
    def providers(
        self,
    ) -> tuple[
        BaseProvider,
        ...
    ]:

        return tuple(
            self._providers.values()
        )

    # ---------------------------------------------------------

    @property
    def repositories(
        self,
    ) -> RepositoryRegistry:

        return self._repositories

    # ---------------------------------------------------------

    @property
    def validators(
        self,
    ) -> tuple[
        BaseValidator,
        ...
    ]:

        return tuple(
            self._validators
        )

    # ---------------------------------------------------------

    def provider_identifiers(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                self._providers.keys()
            )
        )

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._providers.clear()

        self._repositories.clear()

        self._validators.clear()

        self._normalizer = None

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._providers
        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        provider: str,
    ) -> bool:

        return (
            provider.lower()
            in self._providers
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"providers={len(self._providers)}, "
            f"repositories={len(self._repositories)}, "
            f"validators={len(self._validators)})"
        )
