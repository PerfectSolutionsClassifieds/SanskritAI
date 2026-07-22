
from __future__ import annotations

"""
SanskritAI
==========

Repository Registry

Maintains the collection of repository clients available to the
acquisition subsystem.

Responsibilities
----------------
* Register repository clients
* Lookup repositories
* Remove repositories
* Enumerate repositories
* Repository metadata
* Health checks

The registry allows providers and acquisition managers to remain
independent of concrete repository implementations.

Example
-------

registry = RepositoryRegistry()

registry.register(GretilRepositoryClient())

client = registry["gretil"]

client.fetch_catalog()

Future repositories
-------------------

    GretilRepositoryClient
    CologneRepositoryClient
    SaritRepositoryClient
    MuktabodhaRepositoryClient
    SanskritDocumentsRepositoryClient
    GitHubRepositoryClient
    InternetArchiveRepositoryClient

Version
-------
v0.7.0
"""

from __future__ import annotations

from typing import Iterator

from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class RepositoryRegistry:
    """
    Registry of repository clients.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(self) -> None:

        self._repositories: dict[
            str,
            BaseRepositoryClient,
        ] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        repository: BaseRepositoryClient,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register a repository client.
        """

        identifier = repository.identifier.lower()

        if (
            identifier in self._repositories
            and not replace
        ):

            raise ValueError(

                f"Repository '{identifier}' "

                "is already registered."

            )

        self._repositories[
            identifier
        ] = repository

    # ---------------------------------------------------------

    def unregister(
        self,
        identifier: str,
    ) -> bool:
        """
        Remove a repository.
        """

        identifier = identifier.lower()

        if identifier not in self._repositories:

            return False

        del self._repositories[
            identifier
        ]

        return True

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> BaseRepositoryClient | None:

        return self._repositories.get(
            identifier.lower()
        )

    # ---------------------------------------------------------

    def require(
        self,
        identifier: str,
    ) -> BaseRepositoryClient:
        """
        Lookup repository or raise.
        """

        repository = self.get(identifier)

        if repository is None:

            raise KeyError(

                f"Repository '{identifier}' "

                "not registered."

            )

        return repository

    # ---------------------------------------------------------

    def exists(
        self,
        identifier: str,
    ) -> bool:

        return (
            identifier.lower()

            in self._repositories
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def identifiers(
        self,
    ) -> tuple[str, ...]:

        return tuple(

            sorted(

                self._repositories.keys()

            )

        )

    # ---------------------------------------------------------

    def repositories(
        self,
    ) -> tuple[
        BaseRepositoryClient,
        ...
    ]:

        return tuple(

            self._repositories.values()

        )

    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> list[dict]:

        return [

            repository.metadata()

            for repository

            in self._repositories.values()

        ]

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health_report(
        self,
    ) -> dict[str, bool]:
        """
        Ping every repository.
        """

        report: dict[
            str,
            bool,
        ] = {}

        for repository in self._repositories.values():

            try:

                report[
                    repository.identifier

                ] = repository.ping()

            except Exception:

                report[
                    repository.identifier

                ] = False

        return report

    # ---------------------------------------------------------

    def healthy_repositories(
        self,
    ) -> list[
        BaseRepositoryClient
    ]:

        healthy = []

        for repository in self._repositories.values():

            try:

                if repository.ping():

                    healthy.append(repository)

            except Exception:

                continue

        return healthy

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._repositories.clear()

    # ---------------------------------------------------------

    def __contains__(
        self,
        identifier: str,
    ) -> bool:

        return self.exists(identifier)

    # ---------------------------------------------------------

    def __getitem__(
        self,
        identifier: str,
    ) -> BaseRepositoryClient:

        return self.require(identifier)

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[
        BaseRepositoryClient
    ]:

        return iter(

            self._repositories.values()

        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(

            self._repositories

        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"repositories={len(self)})"

        )
