
from __future__ import annotations

"""
SanskritAI
==========

Checksum Validator

Validates downloaded files using cryptographic checksums.

Supported algorithms:

    • SHA-256 (recommended)
    • SHA-1
    • MD5

Responsibilities
----------------
* Compute file digests
* Compare against expected checksums
* Update AcquisitionResult

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from pathlib import Path
import hashlib

from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult
from SanskritAI.acquisition.validators.base_validator import BaseValidator


class ChecksumValidator(BaseValidator):
    """
    Validates downloaded files using checksums.
    """

    DEFAULT_BUFFER_SIZE = 1024 * 1024  # 1 MB

    SUPPORTED_ALGORITHMS = {
        "sha256": hashlib.sha256,
        "sha1": hashlib.sha1,
        "md5": hashlib.md5,
    }

    # ------------------------------------------------------------------
    # BaseValidator API
    # ------------------------------------------------------------------

    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if checksum information is available.
        """
        return (
            manifest.checksum is not None
            and manifest.checksum_algorithm is not None
        )

    def validate(
        self,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> AcquisitionResult:
        """
        Validates downloaded files against the expected checksum.
        """

        if not self.supports(manifest):
            self.add_warning(
                result,
                "Checksum not specified; validation skipped."
            )
            return result

        algorithm_name = manifest.checksum_algorithm.lower()

        algorithm_factory = self.SUPPORTED_ALGORITHMS.get(
            algorithm_name
        )

        if algorithm_factory is None:
            self.add_error(
                result,
                f"Unsupported checksum algorithm: "
                f"{manifest.checksum_algorithm}"
            )
            return result

        try:
            downloaded_files = self.require_downloads(result)

            # Currently validate the primary downloaded file.
            target = downloaded_files[0]

            self.require_file(target)

            actual = self._compute_checksum(
                target,
                algorithm_factory,
            )

            expected = manifest.checksum.lower()

            if actual.lower() == expected:
                result.checksum_verified = True
            else:
                self.add_error(
                    result,
                    (
                        "Checksum mismatch for "
                        f"{target.name}\n"
                        f"Expected: {expected}\n"
                        f"Actual:   {actual}"
                    ),
                )

        except Exception as exc:
            self.add_error(result, str(exc))

        return result

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _compute_checksum(
        self,
        path: Path,
        algorithm_factory,
    ) -> str:
        """
        Computes the checksum of a file.
        """

        digest = algorithm_factory()

        with path.open("rb") as stream:

            while True:

                chunk = stream.read(self.DEFAULT_BUFFER_SIZE)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @classmethod
    def supported_algorithms(cls) -> tuple[str, ...]:
        """
        Returns supported checksum algorithms.
        """
        return tuple(sorted(cls.SUPPORTED_ALGORITHMS.keys()))

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        algorithms = ", ".join(
            sorted(self.SUPPORTED_ALGORITHMS.keys())
        )

        return (
            f"ChecksumValidator("
            f"algorithms=[{algorithms}])"
        )
