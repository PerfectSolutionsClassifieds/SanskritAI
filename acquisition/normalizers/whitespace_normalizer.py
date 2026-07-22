
from __future__ import annotations

"""
SanskritAI
==========

Whitespace Normalizer

Normalizes whitespace within acquired Sanskrit corpus resources.

Responsibilities
----------------
* Normalize horizontal whitespace
* Convert tabs to spaces
* Remove trailing whitespace
* Remove leading whitespace (optional)
* Collapse multiple blank lines
* Preserve intentional paragraph boundaries

This normalizer intentionally does NOT perform:

    • Unicode normalization
    • Sanskrit normalization
    • OCR correction
    • Sandhi processing
    • Parsing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

import re

from SanskritAI.acquisition.normalizers.base_normalizer import (
    BaseNormalizer,
)


class WhitespaceNormalizer(BaseNormalizer):
    """
    Normalizes whitespace while preserving the logical structure
    of Sanskrit texts.
    """

    def __init__(
        self,
        *,
        tab_size: int = 4,
        strip_leading: bool = False,
        strip_trailing: bool = True,
        collapse_blank_lines: bool = True,
        max_consecutive_blank_lines: int = 1,
        collapse_internal_spaces: bool = True,
    ) -> None:
        super().__init__()

        if tab_size <= 0:
            raise ValueError("tab_size must be positive.")

        if max_consecutive_blank_lines < 0:
            raise ValueError(
                "max_consecutive_blank_lines must be >= 0."
            )

        self._tab_size = tab_size
        self._strip_leading = strip_leading
        self._strip_trailing = strip_trailing
        self._collapse_blank_lines = collapse_blank_lines
        self._max_blank_lines = max_consecutive_blank_lines
        self._collapse_internal_spaces = collapse_internal_spaces

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def tab_size(self) -> int:
        return self._tab_size

    @property
    def strip_leading(self) -> bool:
        return self._strip_leading

    @property
    def strip_trailing(self) -> bool:
        return self._strip_trailing

    @property
    def collapse_blank_lines(self) -> bool:
        return self._collapse_blank_lines

    # ---------------------------------------------------------
    # BaseNormalizer API
    # ---------------------------------------------------------

    def normalize(
        self,
        text: str,
    ) -> str:

        text = self.ensure_text(text)

        if not text:
            return text

        #
        # Expand tabs.
        #

        text = text.expandtabs(self._tab_size)

        #
        # Process each line independently.
        #

        lines = []

        for line in text.split("\n"):

            if self._collapse_internal_spaces:
                #
                # Collapse repeated horizontal whitespace.
                #
                line = re.sub(
                    r"[ \t]+",
                    " ",
                    line,
                )

            if self._strip_leading:
                line = line.lstrip()

            if self._strip_trailing:
                line = line.rstrip()

            lines.append(line)

        text = "\n".join(lines)

        if self._collapse_blank_lines:
            text = self._collapse_blank_lines_fn(text)

        return text

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _collapse_blank_lines_fn(
        self,
        text: str,
    ) -> str:
        """
        Limits consecutive blank lines.
        """

        output: list[str] = []

        blank_count = 0

        for line in text.split("\n"):

            if line == "":

                blank_count += 1

                if blank_count <= self._max_blank_lines:
                    output.append("")

            else:

                blank_count = 0
                output.append(line)

        return "\n".join(output)

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    @staticmethod
    def normalize_string(
        text: str,
        **kwargs,
    ) -> str:
        """
        Convenience static API.
        """
        return WhitespaceNormalizer(
            **kwargs,
        ).normalize(text)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "WhitespaceNormalizer("
            f"tab_size={self._tab_size}, "
            f"strip_leading={self._strip_leading}, "
            f"strip_trailing={self._strip_trailing}, "
            f"collapse_blank_lines="
            f"{self._collapse_blank_lines}, "
            f"max_blank_lines={self._max_blank_lines}, "
            f"collapse_internal_spaces="
            f"{self._collapse_internal_spaces})"
        )
