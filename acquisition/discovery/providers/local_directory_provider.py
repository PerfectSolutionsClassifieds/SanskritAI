
from __future__ import annotations
from SanskritAI.acquisition.detectors.source_format_detector import (
    SourceFormatDetector,
)

"""
SanskritAI
==========

Local Directory Provider

Discovers Sanskrit corpus resources stored in one or more local
directories.

Responsibilities
----------------
* Recursively scan directories
* Identify supported corpus files
* Create CorpusSource objects
* Return discovered resources

This provider intentionally does NOT:

    • download files
    • validate resources
    • normalize content
    • parse corpora

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.discovery.base_discovery_provider import (
    BaseDiscoveryProvider,
)
from SanskritAI.acquisition.factories.corpus_source_factory import (
    CorpusSourceFactory,
)

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType


class LocalDirectoryProvider(BaseDiscoveryProvider):
    """
    Discovers corpus resources from local directories.
    """

    # DEFAULT_EXTENSIONS = {
    #     ".txt": SourceFormat.TEXT,
    #     ".xml": SourceFormat.XML,
    #     ".tei": SourceFormat.TEI,
    #     ".json": SourceFormat.JSON,
    #     ".csv": SourceFormat.CSV,
    #     ".pdf": SourceFormat.PDF,
    #     ".zip": SourceFormat.ZIP,
    # }

    def __init__(
        self,
        *directories: str | Path,
        recursive: bool = True,
    ) -> None:

        super().__init__()

        self._directories = [
            Path(d).expanduser().resolve()
            for d in directories
        ]

        self._recursive = recursive

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def directories(self) -> tuple[Path, ...]:
        return tuple(self._directories)

    @property
    def recursive(self) -> bool:
        return self._recursive

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(self) -> Iterable[CorpusSource]:

        discovered: list[CorpusSource] = []

        for directory in self._directories:

            if not directory.exists():
                continue

            if not directory.is_dir():
                continue

            iterator = (
                directory.rglob("*")
                if self._recursive
                else directory.glob("*")
            )

            for path in iterator:

                if not path.is_file():
                    continue

                #fmt = self._detect_format(path)
                fmt = SourceFormatDetector.detect(path)


                if fmt is None:
                    continue

                discovered.append(
                    #self._create_source(path, fmt)
                    CorpusSourceFactory.from_file(path)
                )

        return discovered

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    # def _detect_format(
    #     self,
    #     path: Path,
    # ) -> SourceFormat | None:

    #     return self.DEFAULT_EXTENSIONS.get(
    #         path.suffix.lower()
    #     )

    # def _create_source(
    #     self,
    #     path: Path,
    #     fmt: SourceFormat,
    # ) -> CorpusSource:

    #     return CorpusSource(
    #         identifier=str(path.resolve()),
    #         title=path.stem,
    #         source_type=SourceType.LOCAL,
    #         source_format=fmt,
    #         status=SourceStatus.AVAILABLE,
    #         local_path=path,
    #         download_url=None,
    #         checksum=None,
    #         description=None,
    #         license=None,
    #         metadata={
    #             "directory": str(path.parent),
    #             "size": path.stat().st_size,
    #         },
    #     )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "LocalDirectoryProvider("
            f"directories={len(self._directories)}, "
            f"recursive={self._recursive})"
        )
