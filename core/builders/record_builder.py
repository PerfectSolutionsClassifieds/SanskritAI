from __future__ import annotations

"""
SanskritAI
==========

Record Builder

Defines the abstract adapter responsible for transforming
immutable DataRecord objects into validated domain objects.

This class specializes ValidatedBuilder for record-driven
construction while remaining independent of any particular
domain (Corpus, Lexical, Amarakośa, etc.).

Typical pipeline
----------------

Parser
    ↓
DataRecord
    ↓
RecordBuilder
    ↓
Domain Object
    ↓
Registry

Concrete subclasses perform the actual adaptation from a
specific record type to a specific domain model.

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.builders.validated_builder import (
    ValidatedBuilder,
)
from SanskritAI.core.records.data_record import (
    DataRecord,
)
from SanskritAI.core.typing import TObject, TIdentifier


class RecordBuilder(
    ValidatedBuilder[TIdentifier, TObject],
    Generic[TIdentifier, TObject],
    ABC,
):
    """
    Abstract base class for all record-driven builders.

    A RecordBuilder adapts immutable DataRecord instances into
    validated domain objects.

    Subclasses should implement the ``build()`` method inherited
    from ValidatedBuilder.
    """

    @property
    def record_type(self) -> type[DataRecord[TIdentifier]]:
        """
        Returns the record type supported by this builder.

        Concrete builders may override this property to expose
        their supported record type for registration or dynamic
        dispatch.
        """
        return DataRecord
