"""
SanskritAI
==========

Module:
    models.imports.import_configuration

Description
-----------
Configuration object controlling importer behavior.

Every importer in SanskritAI accepts an ImportConfiguration
instance to customize parsing, validation, normalization,
and repository integration.

This class is intentionally generic so that it can be reused
by Amarakośa, Purāṇas, Vedas, dictionaries, and future
corpora.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ImportConfiguration:
    """
    Configuration controlling the import process.

    The default values are conservative and suitable for
    most textual imports.
    """

    # ---------------------------------------------------------
    # Text Processing
    # ---------------------------------------------------------

    normalize_unicode: bool = True

    strip_whitespace: bool = True

    strip_blank_lines: bool = True

    strip_comments: bool = False

    preserve_line_numbers: bool = True

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validate_structure: bool = True

    validate_identifiers: bool = True

    validate_duplicates: bool = True

    fail_on_error: bool = False

    # ---------------------------------------------------------
    # Lexical Processing
    # ---------------------------------------------------------

    build_lexemes: bool = False

    build_relations: bool = False

    tokenize: bool = False

    # ---------------------------------------------------------
    # Repository Integration
    # ---------------------------------------------------------

    update_repository: bool = False

    replace_existing: bool = False

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    verbose: bool = True

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def validation_enabled(self) -> bool:
        """
        True if any validation step is enabled.
        """

        return any(
            (
                self.validate_structure,
                self.validate_identifiers,
                self.validate_duplicates,
            )
        )

    @property
    def lexical_processing_enabled(self) -> bool:
        """
        True if lexical analysis will occur.
        """

        return any(
            (
                self.tokenize,
                self.build_lexemes,
                self.build_relations,
            )
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "normalize_unicode": self.normalize_unicode,

            "strip_whitespace": self.strip_whitespace,

            "strip_blank_lines": self.strip_blank_lines,

            "strip_comments": self.strip_comments,

            "preserve_line_numbers": self.preserve_line_numbers,

            "validate_structure": self.validate_structure,

            "validate_identifiers": self.validate_identifiers,

            "validate_duplicates": self.validate_duplicates,

            "fail_on_error": self.fail_on_error,

            "build_lexemes": self.build_lexemes,

            "build_relations": self.build_relations,

            "tokenize": self.tokenize,

            "update_repository": self.update_repository,

            "replace_existing": self.replace_existing,

            "verbose": self.verbose,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "ImportConfiguration("
            f"validation={self.validation_enabled}, "
            f"lexical={self.lexical_processing_enabled}, "
            f"repository={self.update_repository})"
        )
