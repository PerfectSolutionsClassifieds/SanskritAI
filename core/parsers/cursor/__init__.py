"""
SanskritAI
==========

Parser Cursor Kernel

The cursor subsystem provides navigation over immutable
TokenStream instances.

Responsibilities
----------------
- Cursor navigation
- Look-ahead
- Backtracking
- Checkpoint management
- Parser state isolation

Pipeline
--------

TokenStream
      ↓
ParserCursor
      ↓
Parser
      ↓
Records

Version
-------
v0.6.0
"""

from .cursor_mark import CursorMark
from .cursor_state import CursorState
from .parser_cursor import ParserCursor
from .cursor_exception import CursorException

__all__ = [
    "CursorMark",
    "CursorState",
    "ParserCursor",
    "CursorException",
]
