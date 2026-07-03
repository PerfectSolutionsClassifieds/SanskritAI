class SanskritAIError(Exception):
    """Base project exception."""


class DictionaryFormatError(SanskritAIError):
    """Raised when dictionary data cannot be parsed."""
