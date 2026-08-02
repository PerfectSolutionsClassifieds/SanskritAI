from __future__ import annotations

"""
SanskritAI

Mock Subject

Minimal linguistic object used by Paninian
unit tests.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MockSubject:
    """
    Minimal derivation subject.
    """

    text: str = ""

    category: str = "mock"

    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def __str__(self):
        return self.text
