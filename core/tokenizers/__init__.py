"""
SanskritAI
==========

Tokenizer Kernel

The tokenizer layer is responsible for transforming raw textual
sources into a stream of tokenizer tokens.

Pipeline
--------

Raw Text
    ↓
Tokenizer
    ↓
TokenizerToken
    ↓
TokenStream
    ↓
Parser
    ↓
DataRecord

The tokenizer kernel is intentionally language-agnostic and is
shared by all SanskritAI subsystems, including:

- Corpus
- Lexical
- Amarakośa
- Morphological Engine
- Padaccheda Engine
- OCR Importers
- Future NLP pipelines

Version
-------
v0.6.0
"""

from .token_type import TokenType
from .token_position import TokenPosition
from .tokenizer_token import TokenizerToken
from .token_stream import TokenStream
from .tokenizer import Tokenizer
from .base_tokenizer import BaseTokenizer
from .tokenization_result import TokenizationResult

__all__ = [
    "TokenType",
    "TokenPosition",
    "TokenizerToken",
    "TokenStream",
    "Tokenizer",
    "BaseTokenizer",
    "TokenizationResult",
]
