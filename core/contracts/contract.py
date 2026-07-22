from __future__ import annotations

"""
SanskritAI
==========

Contract

Defines the root architectural contract for all SanskritAI
capability contracts.

A Contract specifies *what* a component is expected to provide,
without prescribing *how* that capability is implemented.

All architectural contracts inherit from this class.

Architecture
------------

Contract
    ├── Identifiable
    ├── Validatable
    ├── Buildable
    ├── Processable
    ├── Parsable
    ├── Tokenizable
    ├── Serializable
    ├── Searchable
    └── Displayable

Notes
-----
Contracts define architectural capabilities.

They are intentionally lightweight and contain no domain
logic or implementation details.

Version
-------
v0.6.0
"""

from abc import ABC


class Contract(ABC):
    """
    Root architectural contract.
    """

    @property
    def contract_name(self) -> str:
        """
        Returns the canonical contract name.
        """
        return self.__class__.__name__

    @property
    def contract_module(self) -> str:
        """
        Returns the module defining this contract.
        """
        return self.__class__.__module__

    @property
    def contract_qualified_name(self) -> str:
        """
        Returns the fully-qualified contract name.
        """
        return (
            f"{self.contract_module}."
            f"{self.contract_name}"
        )

    @property
    def is_contract(self) -> bool:
        """
        Indicates that this type represents an architectural
        contract.
        """
        return True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            "()"
        )
