"""
SanskritAI
==========

Module:
    models.enums.relation_type

Description:
    Canonical lexical and semantic relationship types used throughout
    the SanskritAI platform.

    These relationships connect Lexeme objects and form the basis for
    dictionary linking, Amarakośa integration, semantic search,
    ontology construction, and future knowledge graph development.

Version:
    v0.3.0 Final

Author:
    SanskritAI Project
"""

from enum import Enum


class RelationType(str, Enum):
    """
    Canonical relationship types between Lexeme objects.

    The enum is intentionally broad so that it can be reused by
    dictionaries, ontology modules, and future AI components.
    """

    # ---------------------------------------------------------
    # Semantic Relations
    # ---------------------------------------------------------

    SYNONYM = "synonym"
    ANTONYM = "antonym"

    HYPERNYM = "hypernym"
    HYPONYM = "hyponym"

    MERONYM = "meronym"
    HOLONYM = "holonym"

    RELATED = "related"

    # ---------------------------------------------------------
    # Lexical Relations
    # ---------------------------------------------------------

    VARIANT = "variant"

    ALTERNATE_SPELLING = "alternate_spelling"

    INFLECTION = "inflection"

    ROOT = "root"

    DERIVED_FROM = "derived_from"

    DERIVED_TO = "derived_to"

    COGNATE = "cognate"

    # ---------------------------------------------------------
    # Literary Relations
    # ---------------------------------------------------------

    EPITHET = "epithet"

    TITLE = "title"

    ALIAS = "alias"

    HONORIFIC = "honorific"

    # ---------------------------------------------------------
    # Taxonomic Relations
    # ---------------------------------------------------------

    INSTANCE_OF = "instance_of"

    HAS_INSTANCE = "has_instance"

    CATEGORY = "category"

    MEMBER_OF = "member_of"

    # ---------------------------------------------------------
    # Dictionary-specific Relations
    # ---------------------------------------------------------

    SEE_ALSO = "see_also"

    CROSS_REFERENCE = "cross_reference"

    COMMENTARY = "commentary"

    EXAMPLE = "example"

    # ---------------------------------------------------------
    # Custom / Extension
    # ---------------------------------------------------------

    CUSTOM = "custom"

    UNKNOWN = "unknown"

    @classmethod
    def values(cls) -> list[str]:
        """
        Return all enum values.

        Returns
        -------
        list[str]
            List of relation type values.
        """
        return [member.value for member in cls]

    @classmethod
    def names(cls) -> list[str]:
        """
        Return all enum names.

        Returns
        -------
        list[str]
            List of enum member names.
        """
        return [member.name for member in cls]

    @classmethod
    def has_value(cls, value: str) -> bool:
        """
        Check whether a string is a valid relation type.

        Parameters
        ----------
        value : str

        Returns
        -------
        bool
        """
        return value in cls.values()
