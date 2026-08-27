
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Contract
-------------------------------

Defines the acquisition boundary for Monier-Williams source data.

The source layer is responsible only for obtaining source content.
It must not perform lexical normalization, repository writes, or
linguistic reasoning.

Compatibility
-------------

The source contract supports both:

    1. modern implementations providing ``read()``
    2. legacy/lightweight implementations providing ``acquire()``

This is intentional so that simple test doubles and existing source
implementations remain valid.
"""


class MonierWilliamsSource:
    """Acquisition contract for Monier-Williams source data."""

    SOURCE = "monier-williams"

    @property
    def source(self) -> str:
        """Canonical source identifier."""
        return self.SOURCE

    @property
    def identifier(self) -> str:
        """Stable source identifier."""
        return self.SOURCE

    @property
    def source_name(self) -> str:
        """Human-readable source name."""
        return "Monier-Williams"

    def read(self) -> str:
        """
        Read and return the complete raw source representation.

        Concrete modern implementations may override this method.

        The method intentionally remains non-abstract so lightweight
        compatibility implementations that provide only ``acquire()``
        can still satisfy the source contract.
        """
        raise NotImplementedError(
            "MonierWilliamsSource.read() must be implemented "
            "unless acquire() is overridden."
        )

    def acquire(self) -> str:
        """
        Acquire and return the raw source representation.

        Compatibility alias for implementations based on ``read()``.

        Subclasses may override ``acquire()`` directly.
        """
        return self.read()
