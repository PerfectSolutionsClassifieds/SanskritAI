from __future__ import annotations

"""
SanskritAI
==========

Default Source Acquirer
=======================

Concrete acquisition implementation for AcquisitionManifest.

Responsibilities
----------------
• Resolve primary URLs and mirrors.
• Download the source resource.
• Store the acquired resource at the manifest destination.
• Respect overwrite_existing.
• Record acquisition information in AcquisitionResult.
• Validate checksums when requested.
• Update CorpusSource lifecycle status.
• Remain independent of parsing, normalization and importing.

The implementation intentionally uses Python's standard library
urllib facilities so that the acquisition kernel has no mandatory
third-party HTTP dependency.

Version
-------
v0.5.0
"""

from dataclasses import dataclass
from hashlib import new as hashlib_new
from pathlib import Path
from urllib.parse import unquote
from urllib.request import urlopen

from SanskritAI.acquisition.acquirers.source_acquirer import (
    SourceAcquirer,
)

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)

from SanskritAI.acquisition.models.source_status import (
    SourceStatus,
)


@dataclass(slots=True)
class DefaultSourceAcquirer(
    SourceAcquirer,
):
    """
    Canonical standard-library source acquirer.

    The class performs acquisition only. It does not parse,
    normalize, validate linguistic content, or import data.
    """

    chunk_size: int = 1024 * 64

    # =========================================================
    # Public API
    # =========================================================

    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Acquire the source described by ``manifest``.

        Primary URLs are attempted first, followed by mirrors.

        A failed URL does not immediately terminate acquisition;
        the next configured URL is attempted.

        Returns
        -------
        AcquisitionResult
            Standardized acquisition outcome.
        """

        result = AcquisitionResult(
            source=manifest.source,
        )

        try:
            self._validate_manifest(manifest)

            if not manifest.enabled:
                manifest.source.update_status(
                    SourceStatus.SKIPPED,
                )

                result.success = False
                result.message = (
                    "Acquisition manifest is disabled."
                )
                result.add_warning(
                    "Manifest was skipped because enabled=False."
                )
                return result

            manifest.source.update_status(
                SourceStatus.PENDING_DOWNLOAD,
            )

            urls = manifest.all_urls

            if not urls:
                raise ValueError(
                    "Acquisition manifest contains no URLs."
                )

            destination = self._resolve_destination(
                manifest,
                urls[0],
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if (
                destination.exists()
                and not manifest.overwrite_existing
            ):
                raise FileExistsError(
                    f"Destination already exists: {destination}"
                )

            last_error: Exception | None = None

            for url in urls:
                try:
                    manifest.source.update_status(
                        SourceStatus.DOWNLOADING,
                    )

                    bytes_downloaded = self._download(
                        url=url,
                        destination=destination,
                    )

                    result.bytes_downloaded = (
                        bytes_downloaded
                    )

                    result.add_downloaded_file(
                        destination,
                    )

                    manifest.source.set_local_path(
                        destination,
                    )

                    manifest.source.update_status(
                        SourceStatus.DOWNLOADED,
                    )

                    result.message = (
                        f"Acquisition completed from {url}"
                    )

                    self._validate_checksum(
                        manifest=manifest,
                        path=destination,
                        result=result,
                    )

                    result.finalize()

                    return result

                except Exception as exc:
                    last_error = exc

                    result.add_warning(
                        f"Acquisition attempt failed for "
                        f"{url}: {exc}"
                    )

                    # A failed partial destination must not be
                    # mistaken for a successful acquisition.
                    if destination.exists():
                        try:
                            destination.unlink()
                        except OSError:
                            pass

            if last_error is not None:
                raise last_error

            raise RuntimeError(
                "Acquisition failed without an exception."
            )

        except Exception as exc:
            manifest.source.update_status(
                SourceStatus.FAILED,
            )

            result.add_error(
                str(exc),
            )

            result.message = (
                "Acquisition failed."
            )

            result.finalize()

            return result

    # =========================================================
    # Manifest Validation
    # =========================================================

    def _validate_manifest(
        self,
        manifest: AcquisitionManifest,
    ) -> None:
        """
        Validate the structural requirements needed for
        acquisition.

        This method deliberately performs only acquisition-level
        validation.
        """

        if manifest is None:
            raise ValueError(
                "Acquisition manifest is required."
            )

        if not manifest.manifest_id:
            raise ValueError(
                "Acquisition manifest identifier is required."
            )

        if manifest.source is None:
            raise ValueError(
                "Acquisition manifest source is required."
            )

        if manifest.destination_directory is None:
            raise ValueError(
                "Acquisition destination directory is required."
            )

        if not manifest.all_urls:
            raise ValueError(
                "Acquisition manifest must contain at least "
                "one URL."
            )

    # =========================================================
    # Destination
    # =========================================================

    def _resolve_destination(
        self,
        manifest: AcquisitionManifest,
        url: str,
    ) -> Path:
        """
        Determine the local destination path.
        """

        directory = manifest.destination_directory

        if directory is None:
            raise ValueError(
                "Destination directory is required."
            )

        if manifest.expected_filename:
            filename = Path(
                manifest.expected_filename
            ).name

            if not filename:
                raise ValueError(
                    "Expected filename must not be empty."
                )

            return directory / filename

        filename = self._filename_from_url(
            url,
        )

        if not filename:
            filename = (
                f"{manifest.source.source_id}"
            )

        return directory / filename

    @staticmethod
    def _filename_from_url(
        url: str,
    ) -> str | None:
        """
        Extract a filename from a URL.

        Query strings and fragments are ignored.
        """

        clean_url = url.split(
            "?",
            1,
        )[0].split(
            "#",
            1,
        )[0]

        path = clean_url.rstrip("/")

        if not path:
            return None

        filename = Path(
            unquote(path)
        ).name

        return filename or None

    # =========================================================
    # Download
    # =========================================================

    def _download(
        self,
        *,
        url: str,
        destination: Path,
    ) -> int:
        """
        Download ``url`` into ``destination``.

        Supports standard urllib URL schemes, including
        HTTP(S) and local ``file://`` URLs.
        """

        total = 0

        with urlopen(url) as response:
            with destination.open(
                "wb",
            ) as output:

                while True:
                    chunk = response.read(
                        self.chunk_size,
                    )

                    if not chunk:
                        break

                    output.write(chunk)

                    total += len(chunk)

        return total

    # =========================================================
    # Checksum
    # =========================================================

    def _validate_checksum(
        self,
        *,
        manifest: AcquisitionManifest,
        path: Path,
        result: AcquisitionResult,
    ) -> None:
        """
        Validate the acquired file checksum when requested.

        No checksum means no checksum validation.
        """

        if not manifest.requires_checksum_validation:
            return

        algorithm = (
            manifest.checksum_algorithm
            or "sha256"
        ).lower()

        try:
            digest = hashlib_new(
                algorithm,
            )
        except ValueError as exc:
            raise ValueError(
                f"Unsupported checksum algorithm: "
                f"{algorithm}"
            ) from exc

        with path.open(
            "rb",
        ) as source:

            while True:
                chunk = source.read(
                    self.chunk_size,
                )

                if not chunk:
                    break

                digest.update(chunk)

        actual = digest.hexdigest()
        expected = (
            manifest.checksum or ""
        ).strip().lower()

        if actual != expected:
            raise ValueError(
                "Checksum verification failed: "
                f"expected {expected}, "
                f"got {actual}"
            )

        result.checksum_verified = True
