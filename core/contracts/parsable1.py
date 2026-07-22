from __future__ import annotations

"""
SanskritAI
==========

Parsable Contract

Defines the architectural contract for components capable of
parsing structured or unstructured input into canonical
SanskritAI representations.

Parsing is a specialized form of processing that transforms
input into structured domain objects such as records,
lexemes, synsets, corpus objects, or syntax trees.

This contract extends the generic Processable capability.

Typical implementations include:

- AmarakoshaParser
- CorpusParser
- XMLParser
- JSONParser
- CSVParser
- OCRParser

Architecture
------------

Contract
      │
      ▼
Processable
      │
      ▼
Parsable

Version
-------
v0.6.0
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from SanskritAI.core.contracts.processable import Processable


class Parsable(Processable):
    """
    Architectural contract for parsing components.
    """

    @property
    def can_parse(self) -> bool:
        """
        Indicates that this component supports parsing.
        """
        return True

    @abstractmethod
    def parse(
        self,
        input_data: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Parses the supplied input into one or more structured
        SanskritAI objects.

        Parameters
        ----------
        input_data:
            Input accepted by the parser.

        Returns
        -------
        Any
            Parser-specific result.
        """
        raise NotImplementedError

    def process(
        self,
        input_data: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Parsing is a specialized processing operation.
        """
        return self.parse(input_data, *args, **kwargs)
