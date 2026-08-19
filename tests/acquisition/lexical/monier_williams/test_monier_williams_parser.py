from __future__ import annotations

from SanskritAI.acquisition.lexical.monier_williams import (
    DelimitedMonierWilliamsParser,
)


def test_parse_lines_delegates_to_parse():
    parser = DelimitedMonierWilliamsParser()

    lines = (
        "headword\tdefinition",
        "देव\tgod",
    )

    records = parser.parse_lines(lines)

    assert len(records) == 1
    assert records[0].headword == "देव"
