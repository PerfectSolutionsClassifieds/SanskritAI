
"""
SanskritAI
==========

Repository Clients

Repository clients provide a uniform interface for interacting
with remote Sanskrit corpus repositories.

Examples
--------
    • RemoteRepositoryClient
    • GRETILRepository
    • CologneRepository
    • SARITRepository
    • MuktabodhaRepository

Repository clients intentionally do NOT:

    • parse corpora
    • normalize text
    • validate downloads
    • import corpus data

Those responsibilities belong to later acquisition stages.

Version
-------
v0.5.0
"""

from .remote_repository_client import RemoteRepositoryClient

__all__ = [
    "RemoteRepositoryClient",
]
