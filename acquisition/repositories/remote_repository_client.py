
from __future__ import annotations

"""
SanskritAI
==========

Remote Repository Client

Abstract base class for interacting with remote Sanskrit corpus
repositories.

Responsibilities
----------------
* Manage HTTP sessions
* Build repository URLs
* Perform HTTP requests
* Download metadata
* Provide common repository utilities

Concrete subclasses include:

    • GRETILRepositoryClient
    • CologneRepositoryClient
    • SARITRepositoryClient
    • MuktabodhaRepositoryClient
    • SanskritDocumentsRepositoryClient

This class intentionally does NOT:

    • parse repository responses
    • normalize corpus data
    • import corpora

Version
-------
v0.5.0
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import requests
from requests import Response
from requests import Session


class RemoteRepositoryClient(ABC):
    """
    Base class for remote corpus repositories.
    """

    DEFAULT_TIMEOUT = 30

    DEFAULT_USER_AGENT = (
        "SanskritAI/0.5 "
        "(Corpus Acquisition Framework)"
    )

    def __init__(
        self,
        *,
        base_url: str,
        timeout: int = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
        verify_ssl: bool = True,
    ) -> None:

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._verify_ssl = verify_ssl

        self._session: Session = requests.Session()

        self._session.headers.update(
            {
                "User-Agent": (
                    user_agent
                    or self.DEFAULT_USER_AGENT
                )
            }
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def session(self) -> Session:
        return self._session

    # ---------------------------------------------------------
    # HTTP Helpers
    # ---------------------------------------------------------

    def get(
        self,
        url: str,
        **kwargs: Any,
    ) -> Response:

        response = self._session.get(
            url,
            timeout=self._timeout,
            verify=self._verify_ssl,
            **kwargs,
        )

        response.raise_for_status()

        return response

    def get_text(
        self,
        url: str,
        encoding: str | None = None,
    ) -> str:

        response = self.get(url)

        if encoding:
            response.encoding = encoding

        return response.text

    def get_bytes(
        self,
        url: str,
    ) -> bytes:

        return self.get(url).content

    def download(
        self,
        url: str,
        destination: Path,
    ) -> Path:
        """
        Download a remote resource.
        """

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        response = self.get(
            url,
            stream=True,
        )

        with destination.open("wb") as fp:
            for chunk in response.iter_content(
                chunk_size=8192
            ):
                if chunk:
                    fp.write(chunk)

        return destination

    # ---------------------------------------------------------
    # URL Helpers
    # ---------------------------------------------------------

    def build_url(
        self,
        *parts: str,
    ) -> str:

        cleaned = [
            part.strip("/")
            for part in parts
            if part
        ]

        if not cleaned:
            return self.base_url

        return (
            self.base_url
            + "/"
            + "/".join(cleaned)
        )

    # ---------------------------------------------------------
    # Repository API
    # ---------------------------------------------------------

    @abstractmethod
    def discover(self):
        """
        Discover available corpus resources.

        Returns
        -------
        Iterable[CorpusSource]
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Health Checks
    # ---------------------------------------------------------

    def ping(self) -> bool:
        """
        Returns True if the repository is reachable.
        """

        try:

            response = self.get(self.base_url)

            return response.ok

        except Exception:

            return False

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    def close(self) -> None:

        self._session.close()

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:

        self.close()

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"base_url='{self.base_url}')"
        )
