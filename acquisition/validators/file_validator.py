
from __future__ import annotations

"""
SanskritAI
==========

File Validator

Performs basic validation of downloaded or imported files.

Responsibilities
----------------
* Verify file existence
* Verify regular files
* Verify readability
* Verify non-empty files
* Verify expected filename (optional)
* Verify expected extension (optional)

Does NOT perform:

* checksum verification
* archive validation
* XML validation
* Unicode normalization
* corpus parsing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

import os
from pathlib import Path

from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult
from SanskritAI.acquisition.validators.base_validator import BaseValidator


class FileValidator(BaseValidator):
    """
    Performs generic filesystem validation.
    """

    # ---------------------------------------------------------
    # BaseValidator API
    # ---------------------------------------------------------

    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        File validation is always applicable.
        """
        return True

    def validate(
        self,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> AcquisitionResult:
        """
        Validate every downloaded file.
        """

        try:
            files = self.require_downloads(result)

            for path in files:
                self._validate_file(
                    path,
                    manifest,
                    result,
                )

        except Exception as exc:
            self.add_error(result, str(exc))

        return result

    # ---------------------------------------------------------
    # Internal Validation
    # ---------------------------------------------------------

    def _validate_file(
        self,
        path: Path,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> None:
        """
        Validates one file.
        """

        self.require_file(path)

        self._validate_readable(path)

        self._validate_size(path)

        self._validate_filename(
            path,
            manifest,
            result,
        )

        self._validate_extension(
            path,
            manifest,
            result,
        )

    def _validate_readable(
        self,
        path: Path,
    ) -> None:
        """
        Ensures the file is readable.
        """

        if not os.access(path, os.R_OK):
            raise PermissionError(
                f"File is not readable: {path}"
            )

    def _validate_size(
        self,
        path: Path,
    ) -> None:
        """
        Reject empty files.
        """

        size = path.stat().st_size

        if size <= 0:
            raise ValueError(
                f"Empty file: {path}"
            )

    def _validate_filename(
        self,
        path: Path,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> None:
        """
        Validate expected filename if specified.
        """

        expected = manifest.expected_filename

        if expected is None:
            return

        if path.name != expected:
            self.add_warning(
                result,
                (
                    f"Filename differs from expected "
                    f"('{expected}'): {path.name}"
                ),
            )

    def _validate_extension(
        self,
        path: Path,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> None:
        """
        Validate file extension if expected formats
        are specified.
        """

        expected_formats = getattr(
            manifest,
            "expected_formats",
            None,
        )

        if not expected_formats:
            return

        extension = path.suffix.lower().lstrip(".")

        allowed = {
            fmt.name.lower()
            for fmt in expected_formats
        }

        if extension not in allowed:
            self.add_warning(
                result,
                (
                    f"Unexpected file extension "
                    f"'.{extension}'. "
                    f"Expected one of "
                    f"{sorted(allowed)}."
                ),
            )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @staticmethod
    def is_empty(
        path: Path,
    ) -> bool:
        """
        Returns True if the file is empty.
        """

        return path.stat().st_size == 0

    @staticmethod
    def file_size(
        path: Path,
    ) -> int:
        """
        Returns the file size in bytes.
        """

        return path.stat().st_size

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return "FileValidator()"
