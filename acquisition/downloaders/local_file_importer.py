
from __future__ import annotations

"""
SanskritAI
==========

Local File Importer

Acquires corpus resources from the local filesystem.

Responsibilities
----------------
* Copy local files into the acquisition repository
* Copy entire directories when required
* Record acquired files in AcquisitionResult

Does NOT perform:

* checksum verification
* unicode normalization
* archive extraction
* parsing
* importing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from pathlib import Path
import shutil

from SanskritAI.acquisition.downloaders.base_downloader import BaseDownloader
from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult


class LocalFileImporter(BaseDownloader):
    """
    Acquires corpus resources from local files or directories.
    """

    # ------------------------------------------------------------------
    # BaseDownloader API
    # ------------------------------------------------------------------

    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if the manifest specifies a local source path.
        """
        source_path = manifest.get_metadata("source_path")
        return source_path is not None

    def download(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Copies a local file or directory into the acquisition
        destination.
        """

        result = AcquisitionResult(source=manifest.source)

        source = manifest.get_metadata("source_path")

        if source is None:
            result.add_error(
                "Manifest metadata does not contain 'source_path'."
            )
            return self.finalize_result(result)

        source_path = Path(source)

        if not source_path.exists():
            result.add_error(
                f"Source does not exist: {source_path}"
            )
            return self.finalize_result(result)

        if manifest.destination_directory is None:
            result.add_error(
                "Manifest.destination_directory is not configured."
            )
            return self.finalize_result(result)

        self.validate_destination(
            manifest.destination_directory
        )

        try:
            if source_path.is_file():
                destination = self._copy_file(
                    source_path,
                    manifest,
                )

                result.add_downloaded_file(destination)

                try:
                    result.bytes_downloaded = destination.stat().st_size
                except OSError:
                    pass

            elif source_path.is_dir():
                copied = self._copy_directory(
                    source_path,
                    manifest,
                )

                for file in copied:
                    result.add_downloaded_file(file)

                    try:
                        result.bytes_downloaded += file.stat().st_size
                    except OSError:
                        pass

            else:
                result.add_error(
                    f"Unsupported source: {source_path}"
                )
                return self.finalize_result(result)

            result.message = (
                f"Imported local resource: {source_path}"
            )

        except Exception as exc:
            result.add_error(str(exc))

        return self.finalize_result(result)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _copy_file(
        self,
        source: Path,
        manifest: AcquisitionManifest,
    ) -> Path:
        """
        Copies a single file.
        """

        filename = (
            manifest.expected_filename
            or source.name
        )

        destination = self.destination_file(
            manifest,
            filename,
        )

        self.remove_existing(
            destination,
            manifest.overwrite_existing,
        )

        shutil.copy2(
            source,
            destination,
        )

        return destination

    def _copy_directory(
        self,
        source: Path,
        manifest: AcquisitionManifest,
    ) -> list[Path]:
        """
        Recursively copies a directory.

        Returns the list of copied files.
        """

        destination_root = (
            manifest.destination_directory
            / source.name
        )

        self.remove_existing(
            destination_root,
            manifest.overwrite_existing,
        )

        shutil.copytree(
            source,
            destination_root,
        )

        copied_files: list[Path] = []

        for path in destination_root.rglob("*"):
            if path.is_file():
                copied_files.append(path)

        return copied_files

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return "LocalFileImporter()"
