"""
SanskritAI
==========

Types Kernel

Provides immutable typed value wrappers used throughout the
SanskritAI framework.

Architecture
------------

Type
 │
 ├── StringType
 ├── IntegerType
 └── BooleanType
"""

from SanskritAI.core.types.type import Type
from SanskritAI.core.types.string_type import StringType
from SanskritAI.core.types.integer_type import IntegerType
from SanskritAI.core.types.boolean_type import BooleanType

__all__ = [
    "Type",
    "StringType",
    "IntegerType",
    "BooleanType",
]
