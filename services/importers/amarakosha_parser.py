
"""
SanskritAI
==========

Module:
    services.importers.amarakosha_parser

Description
-----------
Refactored, enterprise-grade orchestrator for the Amarakośa corpus parser.
Leverages the v0.5.0-alpha decoupled architecture design.

Layered Execution:
    Public API -> Engine Loop -> Context FSM -> Domain Builders -> Domain Model

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations
from pathlib import Path
from typing import Callable

from models.imports import ImportConfiguration, ImportResult, ImportStatus

from services.importers.line_classifier import LineClassifier, LineType
from services.importers.unicode_normalizer import UnicodeNormalizer
from services.importers.parser_state import ParserState

# Architectural Layer Components
from services.importers.parser_errors import ParserError, RecoverableParserError, FatalParserError, StructureError
from services.importers.parser_context_v2 import ParserContextV2
from services.importers.amarakosha_builder import AmarakoshaBuilder
from services.importers.parser_validator import ParserValidator
from services.importers.structure_numbering import StructureNumbering
from services.importers.classification_result import ClassificationResult
from services.importers.import_result_builder import ImportResultBuilder

DEFAULT_ENCODING = "utf-8"
SUPPORTED_EXTENSIONS = (".txt",)
Handler = Callable[[ClassificationResult], None]


class AmarakoshaParser:
    """
    Clean, pure orchestration engine for parsing the Amarakośa.
    Delegates all classification, data construction, state rules, and structural validation.
    """

    def __init__(self, configuration: ImportConfiguration | None = None) -> None:
        self.configuration = configuration if configuration is not None else ImportConfiguration()
        
        self._classifier = LineClassifier()
        self._normalizer = UnicodeNormalizer()
        self._context: ParserContextV2 | None = None

        self._handlers: dict[LineType, Handler] = {
            LineType.EMPTY: self._handle_empty,
            LineType.COMMENT: self._handle_comment,
            LineType.KANDA: self._handle_kanda,
            LineType.VARGA: self._handle_varga,
            LineType.VERSE: self._handle_verse,
            LineType.UNKNOWN: self._handle_unknown,
        }

    @property
    def context(self) -> ParserContextV2:
        if self._context is None:
            raise RuntimeError("ParserContext execution layer is uninitialized.")
        return self._context

    # -------------------------------------------------------------------------
    # Public Ingestion APIs
    # -------------------------------------------------------------------------

    def parse_file(self, path: str | Path) -> ImportResult:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(file_path)
        if file_path.suffix and file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Extension format '{file_path.suffix}' not supported.")

        return self.parse_text(file_path.read_text(encoding=DEFAULT_ENCODING))

    def parse_text(self, text: str) -> ImportResult:
        normalized = self._normalizer.normalize(text)
        return self.parse_lines(normalized.splitlines())

    def parse_lines(self, lines: list[str]) -> ImportResult:
        self._context = ParserContextV2()
        status = ImportStatus.SUCCESS

        try:
            self._engine_loop(lines)
            self._finalize_pipeline()
        except FatalParserError as exc:
            self.context.transition(ParserState.ERROR)
            self.context.add_error(f"Fatal Parser Halt: {str(exc)}", severity="fatal")
            status = ImportStatus.FAILED
        except Exception as exc:
            self.context.transition(ParserState.ERROR)
            self.context.add_error(f"System Operational Interruption: {str(exc)}", severity="fatal")
            status = ImportStatus.FAILED

        return (
            ImportResultBuilder()
            .with_status(status if self.context.state != ParserState.ERROR else ImportStatus.FAILED)
            .with_book(self.context.book)
            .with_statistics(self.context.statistics)
            .with_errors(self.context.errors)
            .build()
        )

    # -------------------------------------------------------------------------
    # Pipeline Orchestration Engine
    # -------------------------------------------------------------------------

    def _engine_loop(self, lines: list[str]) -> None:
        self.context.transition(ParserState.EXPECT_KANDA)

        for raw_line in lines:
            self.context.next_line(raw_line)
            
            # Layer 3 Pipeline: Normalize -> Classify & Package -> Validate & Dispatch
            line_type = self._classifier.classify(self.context.current_line)
            result = ClassificationResult(line_type=line_type, content=self.context.current_line.strip())
            
            self._dispatch_safely(result)

    def _dispatch_safely(self, result: ClassificationResult) -> None:
        try:
            handler = self._handlers.get(result.line_type, self._handle_unknown)
            handler(result)
        except RecoverableParserError as exc:
            self.context.add_error(str(exc), severity="warning")
        except StructureError as exc:
            self.context.add_error(f"Structural Violation: {str(exc)}", severity="warning")

    # -------------------------------------------------------------------------
    # Layer 4: Action Handlers (Isolated Orchestration)
    # -------------------------------------------------------------------------

    def _handle_kanda(self, result: ClassificationResult) -> None:
        ParserValidator.validate_transition(self.context.state, ParserState.EXPECT_VARGA, self.context.line_number)
        
        num = StructureNumbering.next_kanda_number(self.context.book)
        kanda = AmarakoshaBuilder.build_kanda(number=num, title=result.content)
        
        self.context.enter_kanda(kanda)
        self.context.transition(ParserState.EXPECT_VARGA)

    def _handle_varga(self, result: ClassificationResult) -> None:
        ParserValidator.validate_transition(self.context.state, ParserState.EXPECT_VERSE, self.context.line_number)
        ParserValidator.validate_hierarchy_presence(self.context.current_kanda, "Varga", self.context.line_number)
        
        num = StructureNumbering.next_varga_number(self.context.current_kanda)
        varga = AmarakoshaBuilder.build_varga(number=num, title=result.content)
        
        self.context.enter_varga(varga)
        self.context.transition(ParserState.EXPECT_VERSE)

    def _handle_verse(self, result: ClassificationResult) -> None:
        ParserValidator.validate_transition(self.context.state, ParserState.EXPECT_VERSE, self.context.line_number)
        ParserValidator.validate_hierarchy_presence(self.context.current_varga, "Verse", self.context.line_number)
        
        num = StructureNumbering.next_verse_number(self.context.current_varga)
        verse = AmarakoshaBuilder.build_verse(number=num, text=result.content)
        
        self.context.enter_verse(verse)
        self.context.transition(ParserState.EXPECT_VERSE)

    def _handle_empty(self, result: ClassificationResult) -> None:
        self.context.statistics.empty_lines += 1

    def _handle_comment(self, result: ClassificationResult) -> None:
        self.context.statistics.comment_lines += 1

    def _handle_unknown(self, result: ClassificationResult) -> None:
        self.context.statistics.unknown_lines += 1
        self.context.add_error(f"Lexical analysis unknown token match: {result.content}", severity="warning")

    # -------------------------------------------------------------------------
    # Layer 5: Clean Finalization Pipeline
    # -------------------------------------------------------------------------

    def _finalize_pipeline(self) -> None:
        self.context.transition(ParserState.FINISHED)
        
        # Tree hierarchy validation check
        warnings = ParserValidator.validate_completion(self.context.book)
        for warn_msg in warnings:
            self.context.add_error(warn_msg, severity="warning")

    def __repr__(self) -> str:
        if self._context is None:
            return "AmarakoshaParser(state=UNINITIALIZED)"
        return (
            f"AmarakoshaParser("
            f"state={self.context.state.name}, "
            f"line={self.context.line_number}, "
            f"kandas={self.context.statistics.kandas}, "
            f"vargas={self.context.statistics.vargas}, "
            f"verses={self.context.statistics.verses}, "
            f"errors={len(self.context.errors)}"
            f")"
        )
