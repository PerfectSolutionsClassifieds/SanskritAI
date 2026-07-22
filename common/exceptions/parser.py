from __future__ import annotations

"""
SanskritAI
==========

Parser Exceptions

Exceptions related to parsing of
TXT, XML, HTML, TEI, PDF and other
input formats.
"""

from SanskritAI.common.exceptions.sanskrit_ai_exception import (
    SanskritAIException,
)


class ParserException(SanskritAIException):
    """
    Base parser exception.
    """
    pass


class XMLParserException(ParserException):
    """
    XML parsing failure.
    """
    pass


class HTMLParserException(ParserException):
    """
    HTML parsing failure.
    """
    pass


class TEIParserException(ParserException):
    """
    TEI parsing failure.
    """
    pass


class PDFParserException(ParserException):
    """
    PDF parsing failure.
    """
    pass


class TextParserException(ParserException):
    """
    Plain-text parsing failure.
    """
    pass
