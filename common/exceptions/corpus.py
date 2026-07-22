from __future__ import annotations

"""
SanskritAI
==========

Corpus Exceptions

Exceptions raised while constructing,
validating or manipulating canonical corpus
objects.
"""

from SanskritAI.common.exceptions.sanskrit_ai_exception import (
    SanskritAIException,
)


class CorpusException(SanskritAIException):
    """
    Base corpus exception.
    """
    pass


class CorpusValidationException(CorpusException):
    """
    Raised when corpus validation fails.
    """
    pass


class DocumentException(CorpusException):
    """
    Raised for document-level errors.
    """
    pass


class SectionException(CorpusException):
    """
    Raised for section-related errors.
    """
    pass


class ChapterException(CorpusException):
    """
    Raised for chapter-related errors.
    """
    pass


class VerseException(CorpusException):
    """
    Raised for verse-related errors.
    """
    pass


class TokenException(CorpusException):
    """
    Raised for token-related errors.
    """
    pass
