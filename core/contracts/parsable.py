from __future__ import annotations

"""
SanskritAI
==========

Parsable Contract

Defines the contract for components capable of parsing an input
source into a structured representation.

Typical implementations include:

- Sanskrit Parser
- XML Parser
- JSON Parser
- Grammar Parser
- Corpus Parser

Architecture
------------

Contract
      │
      ▼
Parsable

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import Any

from SanskritAI.core.contracts.contract import Contract


class Parsable(Contract):
    """
    Contract for parsable components.
    """

    @abstractmethod
    def parse(
        self,
        source: Any,
    ) -> Any:
        """
        Parses the supplied source into a structured result.

        Parameters
        ----------
        source:
            Input to be parsed.

        Returns
        -------
        Any
            Parsed representation.
        """
        raise NotImplementedError
