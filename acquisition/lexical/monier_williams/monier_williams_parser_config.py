
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MonierWilliamsParserConfig:
    """
    Configuration for delimited Monier–Williams source parsing.
    """

    delimiter: str = "\t"

    required_headers: tuple[str, ...] = (
        "headword",
        "definition",
    )

    optional_headers: tuple[str, ...] = (
        "grammatical_category",
        "transliteration",
        "source_reference",
    )

    encoding: str = "utf-8"

    skip_blank_lines: bool = True

    strict_headers: bool = True
