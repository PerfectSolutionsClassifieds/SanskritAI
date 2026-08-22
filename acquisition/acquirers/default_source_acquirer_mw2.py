
from __future__ import annotations

"""
SanskritAI
==========

Default Source Acquirer
=======================

Concrete in-process implementation of SourceAcquirer.

Responsibilities
----------------
• Validate an AcquisitionManifest.
• Try primary URLs followed by mirrors.
• Support HTTP/HTTPS URLs.
• Support local file:// URLs.
• Resolve destination filenames.
• Create destination directories when necessary.
• Respect overwrite_existing.
• Record downloaded files and byte counts.
• Verify optional checksums.
• Update CorpusSource acquisition status.
• Finalize AcquisitionResult.

Important Result Semantics
---------------------------
• A completely successful acquisition returns success=True.
• A disabled manifest returns success=False with SKIPPED status.
• A failed primary URL followed by a successful mirror is a
  successful acquisition with warnings.
• Actual acquisition failures are recorded as errors.
• Existing destination files are rejected unless
  overwrite_existing=True.

The acquirer deliberately does NOT:
    • parse acquired content
    • normalize content
    • import content
    • construct repository objects

Version
-------
v1.1.0
"""

from hashlib import new as hashlib_new
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen
import shutil

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)

from SanskritAI.acquisition.models.source_status import (
    SourceStatus,
)


class DefaultSourceAcquirer:
    """
    Default concrete source acquisition implementation.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Execute the acquisition described by ``manifest``.
        """

        # --------------------------------------------------------------
        # Defensive handling of an invalid None manifest
        # --------------------------------------------------------------

        if manifest is None:
            raise ValueError(
                "Acquisition manifest is required."
            )

        result = AcquisitionResult(
            source=manifest.source,
        )

        try:
            # ----------------------------------------------------------
            # Validate manifest
            # ----------------------------------------------------------

            self._validate_manifest(
                manifest,
                result,
            )

            if result.has_errors:
                manifest.source.update_status(
                    SourceStatus.FAILED,
                )
                return result

            # ----------------------------------------------------------
            # Disabled manifest
            # ----------------------------------------------------------

            if not manifest.enabled:
                manifest.source.update_status(
                    SourceStatus.SKIPPED,
                )

                result.success = False

                result.message = (
                    "Acquisition manifest is disabled."
                )

                return result

            # ----------------------------------------------------------
            # Acquisition lifecycle
            # ----------------------------------------------------------

            manifest.source.update_status(
                SourceStatus.PENDING_DOWNLOAD,
            )

            destination_directory = (
                self._prepare_destination(
                    manifest,
                )
            )

            manifest.source.update_status(
                SourceStatus.DOWNLOADING,
            )

            downloaded_path = (
                self._download_from_sources(
                    manifest=manifest,
                    destination_directory=destination_directory,
                    result=result,
                )
            )

            # ----------------------------------------------------------
            # All URLs failed
            # ----------------------------------------------------------

            if downloaded_path is None:
                manifest.source.update_status(
                    SourceStatus.FAILED,
                )

                if not result.has_errors:
                    result.add_error(
                        "All acquisition URLs failed."
                    )

                result.success = False

                return result

            # ----------------------------------------------------------
            # Download accounting
            # ----------------------------------------------------------

            result.add_downloaded_file(
                downloaded_path,
            )

            result.bytes_downloaded = (
                downloaded_path.stat().st_size
            )

            manifest.source.set_local_path(
                downloaded_path,
            )

            manifest.source.update_status(
                SourceStatus.DOWNLOADED,
            )

            # ----------------------------------------------------------
            # Expected size validation
            # ----------------------------------------------------------

            if (
                manifest.expected_size is not None
                and result.bytes_downloaded
                != manifest.expected_size
            ):
                result.add_error(
                    "Downloaded file size does not match "
                    f"expected size: "
                    f"{manifest.expected_size}; "
                    f"actual: {result.bytes_downloaded}."
                )

                manifest.source.update_status(
                    SourceStatus.FAILED,
                )

                return result

            # ----------------------------------------------------------
            # Checksum validation
            # ----------------------------------------------------------

            if manifest.requires_checksum_validation:
                manifest.source.update_status(
                    SourceStatus.VALIDATING,
                )

                self._verify_checksum(
                    manifest=manifest,
                    path=downloaded_path,
                    result=result,
                )

                if result.has_errors:
                    manifest.source.update_status(
                        SourceStatus.FAILED,
                    )

                    return result

                manifest.source.update_status(
                    SourceStatus.VALIDATED,
                )

            # ----------------------------------------------------------
            # Successful terminal state
            #
            # Explicitly establish success=True.
            # This prevents success state from being dependent on
            # dataclass initialization semantics.
            # ----------------------------------------------------------

            result.success = True

            result.message = (
                "Source acquired successfully."
            )

            return result

        except Exception as exc:

            result.add_error(
                f"Acquisition failed: {exc}"
            )

            result.success = False

            manifest.source.update_status(
                SourceStatus.FAILED,
            )

            return result

        finally:
            result.finalize()

    # ------------------------------------------------------------------
    # Manifest Validation
    # ------------------------------------------------------------------

    def _validate_manifest(
        self,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> None:
        """
        Validate the minimum executable acquisition contract.
        """

        if manifest is None:
            result.add_error(
                "Acquisition manifest is required."
            )
            return

        # Disabled manifests are intentionally not validated
        # as executable acquisition plans.
        if not manifest.enabled:
            return

        if not manifest.source.source_id:
            result.add_error(
                "Source identifier is required."
            )

        if not manifest.all_urls:
            result.add_error(
                "At least one acquisition URL is required."
            )

        if manifest.destination_directory is None:
            result.add_error(
                "Destination directory is required."
            )

    # ------------------------------------------------------------------
    # Destination
    # ------------------------------------------------------------------

    def _prepare_destination(
        self,
        manifest: AcquisitionManifest,
    ) -> Path:
        """
        Prepare and return the destination directory.

        The directory itself may already exist.

        ``overwrite_existing`` applies to an existing acquired
        destination FILE, not to the destination directory itself.
        """

        destination = Path(
            manifest.destination_directory,
        )

        if destination.exists():
            if not destination.is_dir():
                raise ValueError(
                    "Destination path exists and is not "
                    f"a directory: {destination}"
                )

            return destination

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        return destination

    # ------------------------------------------------------------------
    # Download
    # ------------------------------------------------------------------

    def _download_from_sources(
        self,
        manifest: AcquisitionManifest,
        destination_directory: Path,
        result: AcquisitionResult,
    ) -> Path | None:
        """
        Try primary URLs followed by mirrors.

        The first successful acquisition wins.

        Failed candidates before the successful candidate are
        recorded as warnings rather than errors because the
        overall acquisition can still succeed.
        """

        candidate_errors: list[str] = []

        for index, url in enumerate(
            manifest.all_urls,
        ):
            try:
                downloaded_path = self._download_one(
                    url=url,
                    manifest=manifest,
                    destination_directory=destination_directory,
                )

                # ------------------------------------------------------
                # If an earlier URL failed but a later URL succeeded,
                # those failures are warnings.
                # ------------------------------------------------------

                for error in candidate_errors:
                    result.add_warning(
                        f"Acquisition candidate failed: {error}"
                    )

                return downloaded_path

            except Exception as exc:
                candidate_errors.append(
                    f"{url}: {exc}"
                )

        # --------------------------------------------------------------
        # No candidate succeeded.
        # These are genuine acquisition errors.
        # --------------------------------------------------------------

        for error in candidate_errors:
            result.add_error(
                error,
            )

        return None

    # ------------------------------------------------------------------
    # Single URL
    # ------------------------------------------------------------------

    def _download_one(
        self,
        url: str,
        manifest: AcquisitionManifest,
        destination_directory: Path,
    ) -> Path:
        """
        Acquire one URL.
        """

        filename = self._resolve_filename(
            url=url,
            manifest=manifest,
        )

        destination = (
            destination_directory / filename
        )

        # --------------------------------------------------------------
        # Existing destination file
        # --------------------------------------------------------------

        if destination.exists():

            if not manifest.overwrite_existing:
                raise FileExistsError(
                    "Destination file already exists: "
                    f"{destination}"
                )

            if destination.is_dir():
                raise IsADirectoryError(
                    "Destination exists as a directory: "
                    f"{destination}"
                )

        # --------------------------------------------------------------
        # Determine acquisition mechanism
        # --------------------------------------------------------------

        parsed = urlparse(
            url,
        )

        scheme = parsed.scheme.lower()

        if scheme == "file":

            self._copy_local_file(
                url=url,
                destination=destination,
            )

        elif scheme in {
            "http",
            "https",
        }:

            self._download_http(
                url=url,
                destination=destination,
            )

        else:

            raise ValueError(
                "Unsupported acquisition URL scheme: "
                f"{scheme or '<none>'}"
            )

        # --------------------------------------------------------------
        # Verify destination
        # --------------------------------------------------------------

        if not destination.exists():
            raise IOError(
                "Acquisition completed without producing "
                f"destination file: {destination}"
            )

        if not destination.is_file():
            raise IOError(
                "Acquisition destination is not a file: "
                f"{destination}"
            )

        return destination

    # ------------------------------------------------------------------
    # Local file://
    # ------------------------------------------------------------------

    def _copy_local_file(
        self,
        url: str,
        destination: Path,
    ) -> None:
        """
        Copy a local file referenced by a file:// URL.
        """

        parsed = urlparse(
            url,
        )

        source_path = Path(
            unquote(
                parsed.path,
            )
        )

        if not source_path.exists():
            raise FileNotFoundError(
                "Local source does not exist: "
                f"{source_path}"
            )

        if not source_path.is_file():
            raise IsADirectoryError(
                "Local source is not a file: "
                f"{source_path}"
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copyfile(
            source_path,
            destination,
        )

    # ------------------------------------------------------------------
    # HTTP / HTTPS
    # ------------------------------------------------------------------

    def _download_http(
        self,
        url: str,
        destination: Path,
    ) -> None:
        """
        Download an HTTP/HTTPS resource.
        """

        request = Request(
            url,
            headers={
                "User-Agent": (
                    "SanskritAI/1.1 "
                    "(Source Acquirer)"
                )
            },
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with urlopen(
            request,
            timeout=30,
        ) as response:

            with destination.open(
                "wb",
            ) as output:

                shutil.copyfileobj(
                    response,
                    output,
                )

    # ------------------------------------------------------------------
    # Filename
    # ------------------------------------------------------------------

    def _resolve_filename(
        self,
        url: str,
        manifest: AcquisitionManifest,
    ) -> str:
        """
        Resolve destination filename.

        Explicit manifest filename takes precedence.
        """

        if manifest.expected_filename:
            return manifest.expected_filename

        parsed = urlparse(
            url,
        )

        filename = Path(
            unquote(
                parsed.path,
            )
        ).name

        if filename:
            return filename

        raise ValueError(
            "Unable to determine destination filename "
            f"from URL: {url}"
        )

    # ------------------------------------------------------------------
    # Checksum
    # ------------------------------------------------------------------

    def _verify_checksum(
        self,
        manifest: AcquisitionManifest,
        path: Path,
        result: AcquisitionResult,
    ) -> None:
        """
        Verify the downloaded file checksum.
        """

        algorithm = (
            manifest.checksum_algorithm
            .strip()
            .lower()
        )

        expected = (
            manifest.checksum or ""
        ).strip().lower()

        if not expected:
            return

        try:
            digest = hashlib_new(
                algorithm,
            )

        except ValueError as exc:

            result.add_error(
                "Unsupported checksum algorithm "
                f"{algorithm!r}: {exc}"
            )

            return

        with path.open(
            "rb",
        ) as source:

            for chunk in iter(
                lambda: source.read(1024 * 1024),
                b"",
            ):
                digest.update(
                    chunk,
                )

        actual = digest.hexdigest().lower()

        if actual != expected:

            result.add_error(
                "Checksum verification failed: "
                f"expected {expected}, "
                f"actual {actual}."
            )

            return

        result.checksum_verified = True

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )

    def __str__(self) -> str:
        return "Default Source Acquirer"
