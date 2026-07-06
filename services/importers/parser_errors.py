
"""
SanskritAI
==========

Module:
    services.importers.parser_errors

Description
-----------
Domain-specific exceptions for corpus parsing. Separates syntax errors,
structural anomalies, and validation failures from fatal runtime errors.

Version
-------
v0.5.0-alpha
"""

class ParserError(Exception):
    """Base exception for all parsing and validation anomalies."""
    def __init__(self, message: str, line_number: int) -> None:
        super().__init__(message)
        self.line_number = line_number


class RecoverableParserError(ParserError):
    """Errors from which the parser can recover and continue processing lines."""
    pass


class FatalParserError(ParserError):
    """Catastrophic errors that force the parser to abort immediately."""
    pass


class StructureError(RecoverableParserError):
    """Raised when text encounters structural anomalies or invalid nesting."""
    pass


class ValidationError(RecoverableParserError):
    """Raised when domain object completeness checks fail."""
    pass
