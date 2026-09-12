from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Importer

Coordinates parsing, object construction, and registration
for Amarakośa knowledge resources.

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.parsers.amarakosha_parser import (
    AmarakoshaParser,
)
from SanskritAI.amarakosha.registries.amarakosha_registry import (
    AmarakoshaRegistry,
)


class AmarakoshaImporter:
    """
    Orchestrates Amarakośa import workflows.
    """

    def __init__(
        self,
        parser: AmarakoshaParser,
        registry: AmarakoshaRegistry,
    ) -> None:

        self._parser = parser
        self._registry = registry

    # ---------------------------------------------------------

    def import_source(
        self,
        source: str,
    ) -> None:
        """
        Import an Amarakośa source.

        Concrete implementations will:

        1. Parse the source.
        2. Build domain objects.
        3. Register them.
        """
        records = self._parser.parse(source)

        # Builder integration will be added in a subsequent
        # implementation milestone.
        for _record in records:
            pass
