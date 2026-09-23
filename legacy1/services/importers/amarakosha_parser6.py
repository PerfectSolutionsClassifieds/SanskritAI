from pathlib import Path
from typing import List, Optional

from models.imports.import_error import ImportError
from models.imports.import_result import ImportResult, ImportStatus, ImportStatistics
from services.importers.parser_context import ParserContext


class AmarakoshaParser:
    """
    Parser for Amarakośa lexical datasets. Converts raw structural lines into
    parsed entities while building canonical ImportResult diagnostics.
    """

    def __init__(
        self,
        state: Optional[str] = None,
        line: int = 0,
        kandas: int = 0,
        vargas: int = 0,
        verses: int = 0,
        errors: int = 0,
    ) -> None:
        self.state = state
        self.line = line
        self.kandas = kandas
        self.vargas = vargas
        self.verses = verses
        self.errors = errors
        self.context = ParserContext()

    def reset_state(self) -> None:
        """Resets execution state before each parsing run."""
        self.state = "INITIAL"
        self.line = 0
        self.kandas = 0
        self.vargas = 0
        self.verses = 0
        self.errors = 0
        if hasattr(self.context, "reset"):
            self.context.reset()
        else:
            self.context = ParserContext()

    def parse_file(self, file_path: Path) -> ImportResult:
        """Parses an Amarakośa text file and returns an ImportResult."""
        file_path = Path(file_path)
        content = file_path.read_text(encoding="utf-8")
        result = self.parse_text(content)
        result.file = str(file_path)
        return result

    def parse_text(self, text: str) -> ImportResult:
        """Parses a raw string input."""
        normalized = text.strip() if text else ""
        return self.parse_lines(normalized.splitlines() if normalized else [])

    def parse_lines(self, lines: List[str]) -> ImportResult:
        """Parses line-by-line inputs, tracking errors and internal counters."""
        # Fix 1: Reset instance state so pre-existing fixture/instance state is cleared
        self.reset_state()

        try:
            self._engine_loop(lines)
        except Exception as exc:
            # Fix 2: Ensure line_number is >= 1 or None to satisfy ImportError post-init checks
            safe_line = self.line if self.line >= 1 else None
            self.context.add_error(
                message=f"System Operational Interruption: {exc}",
                severity="FATAL",
                line_number=safe_line,
            )

        return self._build_import_result()

    def _engine_loop(self, lines: List[str]) -> None:
        """Internal processing loop for Amarakośa structural content."""
        for idx, raw_line in enumerate(lines, start=1):
            self.line = idx
            line = raw_line.strip()
            if not line:
                continue

            if "काण्ड" in line:
                self.kandas += 1
            elif "वर्ग" in line:
                self.vargas += 1
            elif line.isdigit():
                self.verses += 1
            else:
                # Unknown lines generate recoverable warnings, not fatal errors
                self.context.add_warning(
                    message=f"Unknown input line: '{line}'",
                    line_number=self.line,
                )

    def _build_import_result(self) -> ImportResult:
        """Constructs the canonical ImportResult object from current context."""
        has_errors = self.context.error_count > 0 or self.errors > 0
        status = ImportStatus.FAILED if has_errors else ImportStatus.COMPLETED

        stats = ImportStatistics(
            kandas=self.kandas,
            vargas=self.vargas,
            verses=self.verses,
            errors=self.context.error_count,
            warnings=self.context.warning_count,
        )

        return ImportResult(
            status=status,
            importer="AmarakoshaParser",
            errors=self.context.error_count,
            warnings=self.context.warning_count,
            statistics=stats,
        )
