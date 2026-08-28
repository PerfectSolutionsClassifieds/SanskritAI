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
v0.9.4
"""

from pathlib import Path
from typing import Callable, Any

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
    # Helper Utilities
    # =========================================================

    def _increment_stat(self, stat_name: str, delta: int = 1) -> None:
        """Safely update statistical counter metrics."""
        if hasattr(self.context, "statistics") and self.context.statistics is not None:
            stats = self.context.statistics
            curr = getattr(stats, stat_name, 0)
            try:
                setattr(stats, stat_name, curr + delta)
            except Exception:
                pass
            if isinstance(stats, dict):
                stats[stat_name] = stats.get(stat_name, 0) + delta

        if hasattr(self.context, stat_name):
            try:
                curr = getattr(self.context, stat_name, 0)
                setattr(self.context, stat_name, curr + delta)
            except Exception:
                pass

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
            self._safe_error_transition()
            self.context.add_error(
                f"Fatal Parser Halt: {str(exc)}",
                severity="fatal",
            )
            status = ImportStatus.FAILED

        except Exception as exc:
            self._safe_error_transition()
            self.context.add_error(
                f"System Operational Interruption: {str(exc)}",
                severity="fatal",
            )
            status = ImportStatus.FAILED

        if self.context.state == ParserState.ERROR:
            status = ImportStatus.FAILED

        if any(e.severity in ("ERROR", "FATAL") for e in self.context.errors):
            status = ImportStatus.FAILED

        return (
            ImportResultBuilder()
            .with_status(status)
            .with_imported_object(self.context.book)
            .with_statistics(self.context.statistics)
            .with_errors(self.context.errors)
            .build()
        )

    # ---------------------------------------------------------

    def _safe_error_transition(self) -> None:
        """Ensure contextual consistency during exceptions."""
        try:
            if self.context.state != ParserState.ERROR:
                self.context.transition(ParserState.ERROR)
        except Exception:
            pass

        if self.context.line_number < 1:
            self.context.next_line("")

    # =========================================================
    # Pipeline Orchestration Engine
    # =========================================================

    def _engine_loop(self, lines: list[str]) -> None:
        try:
            self.context.transition(ParserState.EXPECT_KANDA)
        except Exception:
            pass

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

        except Exception as exc:
            self.context.add_error(
                f"Validation Warning: {str(exc)}",
                severity="warning",
            )

    # =========================================================
    # Action Handlers
    # =========================================================

    def _handle_kanda(self, result: ClassificationResult) -> None:
        self._increment_stat("kandas")
        self._increment_stat("objects")

        num = 1
        try:
            if hasattr(StructureNumbering, "next_kanda_number"):
                num = StructureNumbering.next_kanda_number(getattr(self.context, "book", None))
        except Exception:
            pass

        kanda = None
        try:
            if hasattr(AmarakoshaBuilder, "build_kanda"):
                kanda = AmarakoshaBuilder.build_kanda(number=num, title=result.content)
        except Exception:
            pass

        if kanda is not None:
            if hasattr(self.context, "enter_kanda") and callable(getattr(self.context, "enter_kanda")):
                try:
                    self.context.enter_kanda(kanda)
                except Exception:
                    pass

            if hasattr(self.context, "current_kanda"):
                try:
                    setattr(self.context, "current_kanda", kanda)
                except Exception:
                    pass

            book = getattr(self.context, "book", None)
            if book is not None and hasattr(book, "kandas") and isinstance(book.kandas, list):
                if kanda not in book.kandas:
                    book.kandas.append(kanda)

        try:
            self.context.transition(ParserState.EXPECT_VARGA)
        except Exception:
            pass

    # ---------------------------------------------------------

    def _handle_varga(self, result: ClassificationResult) -> None:
        self._increment_stat("vargas")
        self._increment_stat("objects")

        num = 1
        try:
            curr_kanda = getattr(self.context, "current_kanda", None)
            if hasattr(StructureNumbering, "next_varga_number"):
                num = StructureNumbering.next_varga_number(curr_kanda)
        except Exception:
            pass

        varga = None
        try:
            if hasattr(AmarakoshaBuilder, "build_varga"):
                varga = AmarakoshaBuilder.build_varga(number=num, title=result.content)
        except Exception:
            pass

        if varga is not None:
            if hasattr(self.context, "enter_varga") and callable(getattr(self.context, "enter_varga")):
                try:
                    self.context.enter_varga(varga)
                except Exception:
                    pass

            if hasattr(self.context, "current_varga"):
                try:
                    setattr(self.context, "current_varga", varga)
                except Exception:
                    pass

            curr_kanda = getattr(self.context, "current_kanda", None)
            if curr_kanda is not None and hasattr(curr_kanda, "vargas") and isinstance(curr_kanda.vargas, list):
                if varga not in curr_kanda.vargas:
                    curr_kanda.vargas.append(varga)

        try:
            self.context.transition(ParserState.EXPECT_VERSE)
        except Exception:
            pass

    # ---------------------------------------------------------

    def _handle_verse(self, result: ClassificationResult) -> None:
        self._increment_stat("verses")
        self._increment_stat("objects")
        self._increment_stat("lexemes")

        num = 1
        try:
            curr_varga = getattr(self.context, "current_varga", None)
            if hasattr(StructureNumbering, "next_verse_number"):
                num = StructureNumbering.next_verse_number(curr_varga)
        except Exception:
            pass

        verse = None
        try:
            if hasattr(AmarakoshaBuilder, "build_verse"):
                verse = AmarakoshaBuilder.build_verse(number=num, text=result.content)
        except Exception:
            pass

        if verse is not None:
            if hasattr(self.context, "enter_verse") and callable(getattr(self.context, "enter_verse")):
                try:
                    self.context.enter_verse(verse)
                except Exception:
                    pass

            if hasattr(self.context, "current_verse"):
                try:
                    setattr(self.context, "current_verse", verse)
                except Exception:
                    pass

            curr_varga = getattr(self.context, "current_varga", None)
            if curr_varga is not None and hasattr(curr_varga, "verses") and isinstance(curr_varga.verses, list):
                if verse not in curr_varga.verses:
                    curr_varga.verses.append(verse)

        try:
            self.context.transition(ParserState.EXPECT_VERSE)
        except Exception:
            pass

    # ---------------------------------------------------------

    def _handle_empty(self, result: ClassificationResult) -> None:
        self._increment_stat("empty_lines")

    # ---------------------------------------------------------

    def _handle_comment(self, result: ClassificationResult) -> None:
        self._increment_stat("comment_lines")

    # ---------------------------------------------------------

    def _handle_unknown(self, result: ClassificationResult) -> None:
        self._increment_stat("unknown_lines")
        self.context.add_error(
            f"Lexical analysis unknown token match: {result.content}",
            severity="warning",
        )

    # =========================================================
    # Finalization
    # =========================================================

    def _finalize_pipeline(self) -> None:
        try:
            self.context.transition(ParserState.FINISHED)
        except Exception:
            pass

        try:
            warnings = ParserValidator.validate_completion(self.context.book)
            for warn_msg in warnings:
                self.context.add_error(
                    warn_msg,
                    severity="warning",
                )
        except Exception:
            pass

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(self) -> str:
        if self._context is None:
            return "AmarakoshaParser(state=UNINITIALIZED)"

        k = getattr(self.context.statistics, "kandas", 0) if hasattr(self.context, "statistics") else 0
        v = getattr(self.context.statistics, "vargas", 0) if hasattr(self.context, "statistics") else 0
        vs = getattr(self.context.statistics, "verses", 0) if hasattr(self.context, "statistics") else 0
        errs = len(self.context.errors) if hasattr(self.context, "errors") else 0

        state_name = "UNKNOWN"
        if hasattr(self.context, "state") and hasattr(self.context.state, "name"):
            state_name = self.context.state.name

        return (
            "AmarakoshaParser("
            f"state={state_name}, "
            f"line={getattr(self.context, 'line_number', 0)}, "
            f"kandas={k}, "
            f"vargas={v}, "
            f"verses={vs}, "
            f"errors={errs}"
            ")"
        )


        
