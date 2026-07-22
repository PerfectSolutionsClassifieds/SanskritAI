
from __future__ import annotations

"""
SanskritAI
==========

Title Extractor

Extracts the canonical title of a corpus resource.

Extraction priority
-------------------
1. Existing metadata
2. TEI/XML <title> elements
3. HTML <title> element
4. Filename
5. Generic fallback

Version
-------
v0.5.0
"""

from pathlib import Path
from typing import Any
import re
import xml.etree.ElementTree as ET

from SanskritAI.acquisition.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)
from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)


class TitleExtractor(BaseMetadataExtractor):
    """
    Extracts the canonical title of a corpus resource.
    """

    TITLE_PATTERNS = (
        r"<title>(.*?)</title>",
        r"<TITLE>(.*?)</TITLE>",
    )

    # ---------------------------------------------------------
    # Metadata API
    # ---------------------------------------------------------

    def capabilities(self) -> tuple[str, ...]:
        return ("title",)

    # ---------------------------------------------------------
    # Extraction
    # ---------------------------------------------------------

    def extract(
        self,
        source: Path | str | bytes,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> ExtractionResult:

        result = ExtractionResult(
            extractor_name=self.__class__.__name__,
        )

        #
        # Priority 1
        #

        if metadata:

            title = metadata.get("title")

            if isinstance(title, str) and title.strip():

                result.add_metadata("title", title.strip())
                result.confidence = 1.0
                result.finish()
                return result

        #
        # Normalize input
        #

        if isinstance(source, bytes):

            text = source.decode(
                "utf-8",
                errors="replace",
            )

        elif isinstance(source, Path):

            if source.exists():

                try:

                    text = source.read_text(
                        encoding="utf-8",
                        errors="replace",
                    )

                except Exception:

                    text = ""

            else:

                text = ""

        else:

            text = source

        #
        # Priority 2
        # XML / TEI
        #

        title = self._extract_xml_title(text)

        if title:

            result.add_metadata(
                "title",
                title,
            )

            result.confidence = 0.95
            result.finish()

            return result

        #
        # Priority 3
        # HTML
        #

        title = self._extract_html_title(text)

        if title:

            result.add_metadata(
                "title",
                title,
            )

            result.confidence = 0.90
            result.finish()

            return result

        #
        # Priority 4
        # Filename
        #

        if isinstance(source, Path):

            filename = source.stem

        elif isinstance(source, str):

            filename = Path(source).stem

        else:

            filename = None

        if filename:

            filename = self._humanize(filename)

            result.add_metadata(
                "title",
                filename,
            )

            result.confidence = 0.65

            result.finish()

            return result

        #
        # No title found
        #

        result.add_warning(
            "Unable to determine corpus title."
        )

        result.confidence = 0.0

        result.finish()

        return result

    # ---------------------------------------------------------
    # XML
    # ---------------------------------------------------------

    def _extract_xml_title(
        self,
        text: str,
    ) -> str | None:

        try:

            root = ET.fromstring(text)

        except Exception:

            return None

        #
        # Ignore namespaces
        #

        for element in root.iter():

            if element.tag.endswith("title"):

                if element.text:

                    return element.text.strip()

        return None

    # ---------------------------------------------------------
    # HTML
    # ---------------------------------------------------------

    def _extract_html_title(
        self,
        text: str,
    ) -> str | None:

        for pattern in self.TITLE_PATTERNS:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.DOTALL,
            )

            if match:

                return " ".join(
                    match.group(1).split()
                )

        return None

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _humanize(
        filename: str,
    ) -> str:

        filename = filename.replace(
            "_",
            " ",
        )

        filename = filename.replace(
            "-",
            " ",
        )

        filename = re.sub(
            r"\s+",
            " ",
            filename,
        )

        return filename.strip()

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "TitleExtractor()"
