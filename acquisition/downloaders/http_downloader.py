
from __future__ import annotations

"""
SanskritAI
==========

HTTP Downloader

Downloads corpus resources using HTTP or HTTPS.

Responsibilities
----------------
* Download files from remote URLs
* Store files in the destination directory
* Record downloaded files in AcquisitionResult

Does NOT perform:

* checksum verification
* archive extraction
* parsing
* unicode normalization
* importing

Those responsibilities belong to later pipeline stages.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

from SanskritAI.acquisition.downloaders.base_downloader import BaseDownloader
from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult


class HTTPDownloader(BaseDownloader):
    """
    Downloads resources over HTTP/HTTPS.
    """

    DEFAULT_TIMEOUT = 60

    # ---------------------------------------------------------
    # BaseDownloader API
    # ---------------------------------------------------------

    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if the manifest contains at least one
        HTTP or HTTPS URL.
        """
        return any(
            url.startswith(("http://", "https://"))
            for url in manifest.all_urls
        )

    def download(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Download every URL listed in the manifest until one
        succeeds.

        Mirror URLs are attempted automatically if a previous
        URL fails.
        """

        result = AcquisitionResult(source=manifest.source)

        if not manifest.all_urls:
            result.add_error("Manifest contains no download URLs.")
            return self.finalize_result(result)

        last_error: str | None = None

        for url in manifest.all_urls:
            try:
                downloaded = self._download_single(
                    manifest,
                    url,
                )

                result.add_downloaded_file(downloaded)

                try:
                    result.bytes_downloaded += downloaded.stat().st_size
                except OSError:
                    pass

                result.message = f"Downloaded from {url}"

                return self.finalize_result(result)

            except Exception as exc:
                last_error = str(exc)
                result.add_warning(
                    f"Download failed: {url} ({exc})"
                )

        result.add_error(
            last_error or "All download URLs failed."
        )

        return self.finalize_result(result)

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _download_single(
        self,
        manifest: AcquisitionManifest,
        url: str,
    ) -> Path:
        """
        Downloads a single URL.
        """

        filename = self._filename_from_url(
            url,
            manifest.expected_filename,
        )

        destination = self.destination_file(
            manifest,
            filename,
        )

        self.remove_existing(
            destination,
            manifest.overwrite_existing,
        )

        with urlopen(
            url,
            timeout=self.DEFAULT_TIMEOUT,
        ) as response:

            with destination.open("wb") as output:

                while True:

                    chunk = response.read(65536)

                    if not chunk:
                        break

                    output.write(chunk)

        return destination

    @staticmethod
    def _filename_from_url(
        url: str,
        expected: str | None,
    ) -> str:
        """
        Determines the destination filename.
        """

        if expected:
            return expected

        parsed = urlparse(url)

        filename = Path(parsed.path).name

        if filename:
            return filename

        return "download.dat"

    # ---------------------------------------------------------
    # Error formatting
    # ---------------------------------------------------------

    @staticmethod
    def _format_exception(exc: Exception) -> str:

        if isinstance(exc, HTTPError):
            return f"HTTP {exc.code}: {exc.reason}"

        if isinstance(exc, URLError):
            return str(exc.reason)

        return str(exc)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return "HTTPDownloader()"
