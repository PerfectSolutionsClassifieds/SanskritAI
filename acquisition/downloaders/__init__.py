
"""
SanskritAI
==========

Acquisition Downloaders

Provides the download infrastructure used by the acquisition
framework.

Responsibilities
----------------
The downloader subsystem is responsible for obtaining corpus
resources from external or local sources.

Supported download mechanisms include:

    • HTTP / HTTPS
    • Local filesystem
    • (Future) Git repositories
    • (Future) FTP
    • (Future) S3 / Object Storage
    • (Future) Google Drive
    • (Future) Institutional repositories

Downloaders intentionally do NOT perform:

    • Corpus parsing
    • Validation
    • Unicode normalization
    • Database importing

Those responsibilities belong to other layers.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .base_downloader import BaseDownloader
from .http_downloader import HTTPDownloader
from .local_file_importer import LocalFileImporter

__all__ = [
    "BaseDownloader",
    "HTTPDownloader",
    "LocalFileImporter",
]
