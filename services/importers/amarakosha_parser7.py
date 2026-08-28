from __future__ import annotations

"""
SanskritAI
==========

Module:
services.importers.amarakosha_parser

Description
-----------
Refactored, enterprise-grade orchestrator for the Amarakośa corpus parser.

Layered Execution
-----------------
Public API
    ↓
Engine Loop
    ↓
Context FSM
    ↓
Domain Builders
    ↓
Domain Model

Version
-------
v0.9.0
"""

from pathlib import Path
from typing import Callable

from SanskritAI.models.imports import (
    ImportConfiguration,
    ImportResult,
    ImportStatus,
)
from SanskritAI.services.importers.line_classifier import (
    LineClassifier,
    LineType,
)
from SanskritAI.services.importers.unicode_normalizer import (
    UnicodeNormalizer,
)
from SanskritAI.services.importers.parser_state import (
    ParserState,
)
from SanskritAI.services.importers.parser_errors import (
    RecoverableParserError,
    FatalParserError,
    StructureError,
)
from SanskritAI.services.importers.parser_context import (
    ParserContext,
)
from SanskritAI.services.importers.amarakosha_builder import (
    AmarakoshaBuilder,
)
from SanskritAI.services.importers.parser_validator import (
    ParserValidator,
)
from SanskritAI.services.importers.structure_numbering import (
    StructureNumbering,
)
from SanskritAI.services.importers.classification_result import (
    ClassificationResult,
)
from SanskritAI.services.importers.import_result_builder import (
    ImportResultBuilder,
)


DEFAULT_ENCODING = "utf-8"
SUPPORTED_EXTENSIONS = (".txt",)

Handler = Callable[[ClassificationResult], None]


class AmarakoshaParser:
    """
    Clean orchestration engine for parsing the Amarakośa.

    The parser coordinates normalization, classification,
    parser state, structure construction, validation,
    statistics and diagnostics.

    It does not own the canonical corpus identity model.
    """

    def __init__(
        self,
        configuration: ImportConfiguration | None = None,
    ) -> None:
        self.configuration = (
            configuration
            if configuration is not None
            else ImportConfiguration()
        )
        self._classifier = LineClassifier()
        self._normalizer = UnicodeNormalizer()
        self._context: ParserContext | None = None

        self._handlers: dict[LineType, Handler] = {
            LineType.EMPTY: self._handle_empty,
            LineType.COMMENT: self._handle_comment,
            LineType.KANDA: self._handle_kanda,
            LineType.VARGA: self._handle_varga,
            LineType.VERSE: self._handle_verse,
            LineType.UNKNOWN: self._handle_unknown,
        }

    # =========================================================
    # Context
    # =========================================================

    @property
    def context(self) -> ParserContext:
        if self._context is None:
            raise RuntimeError(
                "ParserContext execution layer is uninitialized."
            )
        return self._context

    # =========================================================
    # Public Ingestion APIs
    # =========================================================

    def parse_file(self, path: str | Path) -> ImportResult:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        if (
            file_path.suffix
            and file_path.suffix.lower() not in SUPPORTED_EXTENSIONS
        ):
            raise ValueError(
                f"Extension format '{file_path.suffix}' not supported."
            )

        return self.parse_text(
            file_path.read_text(encoding=DEFAULT_ENCODING)
        )

    # ---------------------------------------------------------

    def parse_text(self, text: str) -> ImportResult:
        normalized = self._normalizer.normalize(text)
        return self.parse_lines(normalized.splitlines())

    # ---------------------------------------------------------

    def parse_lines(self, lines: list[str]) -> ImportResult:
        self._context = ParserContext()
        status = ImportStatus.COMPLETED

        try:
            self._engine_loop(lines)
            self._finalize_pipeline()

        except FatalParserError as exc:
            self.context.transition(ParserState.ERROR)
            self.context.add_error(
                f"Fatal Parser Halt: {str(exc)}",
                severity="fatal",
            )
            status = ImportStatus.FAILED

        except Exception as exc:
            self.context.transition(ParserState.ERROR)
            self.context.add_error(
                f"System Operational Interruption: {str(exc)}",
                severity="fatal",
            )
            status = ImportStatus.FAILED

        return (
            ImportResultBuilder()
            .with_status(
                status
                if self.context.state != ParserState.ERROR
                else ImportStatus.FAILED
            )
            .with_imported_object(self.context.book)
            .with_statistics(self.context.statistics)
            .with_errors(self.context.errors)
            .build()
        )

    # =========================================================
    # Pipeline Orchestration Engine
    # =========================================================

    def _engine_loop(self, lines: list[str]) -> None:
        self.context.transition(ParserState.EXPECT_KANDA)

        for raw_line in lines:
            self.context.next_line(raw_line)
            line_type = self._classifier.classify(self.context.current_line)

            result = ClassificationResult(
                line_type=line_type,
                content=self.context.current_line.strip(),
            )
            self._dispatch_safely(result)

    # ---------------------------------------------------------

    def _dispatch_safely(self, result: ClassificationResult) -> None:
        try:
            handler = self._handlers.get(
                result.line_type,
                self._handle_unknown,
            )
            handler(result)

        except RecoverableParserError as exc:
            self.context.add_error(
                str(exc),
                severity="warning",
            )

        except StructureError as exc:
            self.context.add_error(
                f"Structural Violation: {str(exc)}",
                severity="warning",
            )

    # =========================================================
    # Action Handlers
    # =========================================================

    def _handle_kanda(self, result: ClassificationResult) -> None:
        ParserValidator.validate_transition(
            self.context.state,
            ParserState.EXPECT_VARGA,
            self.context.line_number,
        )

        num = StructureNumbering.next_kanda_number(self.context.book)
        kanda = AmarakoshaBuilder.build_kanda(
            number=num,
            title=result.content,
        )

        self.context.enter_kanda(kanda)
        self.context.transition(ParserState.EXPECT_VARGA)

    # ---------------------------------------------------------

    def _handle_varga(self, result: ClassificationResult) -> None:
        ParserValidator.validate_transition(
            self.context.state,
            ParserState.EXPECT_VERSE,
            self.context.line_number,
        )

        ParserValidator.validate_hierarchy_presence(
            self.context.current_kanda,
            "Varga",
            self.context.line_number,
        )

        num = StructureNumbering.next_varga_number(self.context.current_kanda)
        varga = AmarakoshaBuilder.build_varga(
            number=num,
            title=result.content,
        )

        self.context.enter_varga(varga)
        self.context.transition(ParserState.EXPECT_VERSE)

    # ---------------------------------------------------------

    def _handle_verse(self, result: ClassificationResult) -> None:
        ParserValidator.validate_transition(
            self.context.state,
            ParserState.EXPECT_VERSE,
            self.context.line_number,
        )

        ParserValidator.validate_hierarchy_presence(
            self.context.current_varga,
            "Verse",
            self.context.line_number,
        )

        num = StructureNumbering.next_verse_number(self.context.current_varga)
        verse = AmarakoshaBuilder.build_verse(
            number=num,
            text=result.content,
        )

        self.context.enter_verse(verse)
        self.context.transition(ParserState.EXPECT_VERSE)

    # ---------------------------------------------------------

    def _handle_empty(self, result: ClassificationResult) -> None:
        self.context.statistics.empty_lines += 1

    # ---------------------------------------------------------

    def _handle_comment(self, result: ClassificationResult) -> None:
        self.context.statistics.comment_lines += 1

    # ---------------------------------------------------------

    def _handle_unknown(self, result: ClassificationResult) -> None:
        self.context.statistics.unknown_lines += 1
        self.context.add_error(
            f"Lexical analysis unknown token match: {result.content}",
            severity="warning",
        )

    # =========================================================
    # Finalization
    # =========================================================

    def _finalize_pipeline(self) -> None:
        self.context.transition(ParserState.FINISHED)
        warnings = ParserValidator.validate_completion(self.context.book)

        for warn_msg in warnings:
            self.context.add_error(
                warn_msg,
                severity="warning",
            )

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(self) -> str:
        if self._context is None:
            return "AmarakoshaParser(state=UNINITIALIZED)"

        return (
            "AmarakoshaParser("
            f"state={self.context.state.name}, "
            f"line={self.context.line_number}, "
            f"kandas={self.context.statistics.kandas}, "
            f"vargas={self.context.statistics.vargas}, "
            f"verses={self.context.statistics.verses}, "
            f"errors={len(self.context.errors)}"
            ")"
        )
