
"""
SanskritAI
==========

Module:
    services.importers.amarakosha_parser

Description
-----------
Production-grade parser for the Amarakośa.

This parser transforms the canonical Amarakośa source text into
the SanskritAI object model.

Hierarchy
---------

Amarakosha
    ├── Kanda
    │     ├── Varga
    │     │      ├── Verse
    │     │      ├── Verse
    │     │      └── ...
    │     └── ...
    └── ...

Architecture
------------

Input Text
      │
      ▼
UnicodeNormalizer
      │
      ▼
LineClassifier
      │
      ▼
ParserContext
      │
      ▼
ParserState
      │
      ▼
Dispatcher
      │
      ▼
Domain Model
      │
      ▼
ImportResult

Responsibilities
----------------

• Parse Amarakośa source text
• Detect Kāṇḍa boundaries
• Detect Varga boundaries
• Detect Verse numbering
• Construct canonical object model
• Maintain parser state
• Recover from recoverable errors
• Collect import statistics
• Produce ImportResult

The parser itself is intentionally independent of storage.
Persistence is handled by the Importer layer.

Version
-------
v0.4.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from models.amarakosha import (
    Amarakosha,
    Kanda,
    Varga,
    Verse,
)

from models.imports import (
    ImportConfiguration,
    ImportError,
    ImportResult,
    ImportStatistics,
    ImportStatus,
)

from services.importers.line_classifier import (
    LineClassifier,
    LineType,
)

from SanskritAI.services.importers.parser_context import (
    ParserContext,
)

from services.importers.parser_state import (
    ParserState,
)

from services.importers.unicode_normalizer import (
    UnicodeNormalizer,
)

###############################################################################
# Parser Constants
###############################################################################

DEFAULT_ENCODING = "utf-8"

DEFAULT_BOOK_TITLE = "Amarakośa"

DEFAULT_BOOK_AUTHOR = "Amarasiṃha"

SUPPORTED_EXTENSIONS = (
    ".txt",
)

###############################################################################
# Default Handler Registration
###############################################################################

Handler = Callable[[str], None]

#####Siva1

###############################################################################
# Amarakosha Parser
###############################################################################


class AmarakoshaParser:
    """
    Production-grade Amarakośa parser.

    One parser instance is intended for multiple parsing operations.
    Mutable parsing state is maintained in a ParserContext rather than
    in the parser itself.

    Workflow
    --------

        parse_file()

            │

            ▼

        UnicodeNormalizer

            │

            ▼

        LineClassifier

            │

            ▼

        Dispatcher

            │

            ▼

        Handler Methods

            │

            ▼

        Domain Model

            │

            ▼

        ImportResult
    """

    ###########################################################################
    # Construction
    ###########################################################################

    def __init__(
        self,
        configuration: ImportConfiguration | None = None,
    ) -> None:
        """
        Create a parser.

        Parameters
        ----------
        configuration
            Optional import configuration.

            If omitted, a default ImportConfiguration
            instance is created.
        """

        self.configuration = (
            configuration
            if configuration is not None
            else ImportConfiguration()
        )

        # ---------------------------------------------------------
        # Stateless helper components
        # ---------------------------------------------------------

        self._classifier = LineClassifier()

        self._normalizer = UnicodeNormalizer()

        # ---------------------------------------------------------
        # Mutable parser state
        # ---------------------------------------------------------

        self._context: ParserContext | None = None

        # ---------------------------------------------------------
        # Dispatcher
        # ---------------------------------------------------------

        self._handlers: dict[
            LineType,
            Handler,
        ] = {

            LineType.EMPTY:
                self._handle_empty,

            LineType.COMMENT:
                self._handle_comment,

            LineType.KANDA:
                self._handle_kanda,

            LineType.VARGA:
                self._handle_varga,

            LineType.VERSE:
                self._handle_verse,

            LineType.UNKNOWN:
                self._handle_unknown,
        }

    ###########################################################################
    # Context Initialization
    ###########################################################################

    def _initialize_context(self) -> ParserContext:
        """
        Create a fresh ParserContext.

        A new context is created for every parse operation.

        Returns
        -------
        ParserContext
        """

        context = ParserContext()

        context.book.title = DEFAULT_BOOK_TITLE

        context.book.author = DEFAULT_BOOK_AUTHOR

        context.state = ParserState.START

        self._context = context

        return context

    ###########################################################################
    # Dispatcher
    ###########################################################################

    def _dispatch(
        self,
        line_type: LineType,
        line: str,
    ) -> None:
        """
        Dispatch one classified line.

        Parameters
        ----------
        line_type
            Classification returned by LineClassifier.

        line
            Normalized input line.
        """

        handler = self._handlers.get(line_type)

        if handler is None:

            self._handle_unknown(line)

            return

        handler(line)

    ###########################################################################
    # Internal Helpers
    ###########################################################################

    @property
    def context(self) -> ParserContext:
        """
        Active parser context.

        Raises
        ------
        RuntimeError
            If parsing has not yet been initialized.
        """

        if self._context is None:

            raise RuntimeError(
                "ParserContext has not been initialized."
            )

        return self._context

    @property
    def statistics(self) -> ImportStatistics:
        """
        Convenience accessor.
        """

        return self.context.statistics

    @property
    def book(self) -> Amarakosha:
        """
        Current Amarakosha object.
        """

        return self.context.book

    ###########################################################################
    # Handler Stubs
    #
    # These are implemented in later sections.
    ###########################################################################

    def _handle_empty(
        self,
        line: str,
    ) -> None:
        pass

    def _handle_comment(
        self,
        line: str,
    ) -> None:
        pass

    def _handle_kanda(
        self,
        line: str,
    ) -> None:
        raise NotImplementedError

    def _handle_varga(
        self,
        line: str,
    ) -> None:
        raise NotImplementedError

    def _handle_verse(
        self,
        line: str,
    ) -> None:
        raise NotImplementedError

    def _handle_unknown(
        self,
        line: str,
    ) -> None:
        raise NotImplementedError

#####Siva2        

###############################################################################
# Public API
###############################################################################

    def parse_file(
        self,
        path: str | Path,
    ) -> ImportResult:
        """
        Parse an Amarakośa text file.

        Parameters
        ----------
        path
            Path to a UTF-8 encoded Amarakośa source file.

        Returns
        -------
        ImportResult
        """

        file_path = Path(path)

        if not file_path.exists():

            raise FileNotFoundError(file_path)

        if (
            file_path.suffix
            and file_path.suffix.lower()
            not in SUPPORTED_EXTENSIONS
        ):

            raise ValueError(

                f"Unsupported file extension "

                f"'{file_path.suffix}'."

            )

        text = file_path.read_text(
            encoding=DEFAULT_ENCODING,
        )

        return self.parse_text(text)

    ###########################################################################

    def parse_text(
        self,
        text: str,
    ) -> ImportResult:
        """
        Parse Amarakośa from one text string.

        Parameters
        ----------
        text
            Raw UTF-8 source text.

        Returns
        -------
        ImportResult
        """

        normalized = self._normalizer.normalize(text)

        lines = normalized.splitlines()

        return self.parse_lines(lines)

    ###########################################################################

    def parse_lines(
        self,
        lines: list[str],
    ) -> ImportResult:
        """
        Parse an iterable collection of lines.

        Parameters
        ----------
        lines
            Normalized text lines.

        Returns
        -------
        ImportResult
        """

        context = self._initialize_context()

        try:

            self._parse(lines)

            context.state = ParserState.COMPLETE

            status = ImportStatus.SUCCESS

        except Exception as exc:

            context.state = ParserState.ERROR

            status = ImportStatus.FAILED

            context.add_error(

                ImportError(

                    line_number=context.line_number,

                    message=str(exc),

                    severity="fatal",

                )

            )

        return self._finalize_result(status)

###############################################################################
# Core Parsing Entry Point
###############################################################################

    def _parse(
        self,
        lines: list[str],
    ) -> None:
        """
        Execute the parser.

        This method drives the complete parser state machine.

        Individual line processing is delegated to the
        registered handlers.
        """

        for raw_line in lines:

            self.context.next_line(raw_line)

            line = self.context.current_line

            line_type = self._classifier.classify(line)

            self._dispatch(
                line_type,
                line,
            )

###############################################################################
# Result Construction
###############################################################################

    def _finalize_result(
        self,
        status: ImportStatus,
    ) -> ImportResult:
        """
        Construct the ImportResult returned by the parser.
        """

        return ImportResult(

            status=status,

            book=self.book,

            statistics=self.statistics,

            errors=list(self.context.errors),

        )

#####Siva3

###############################################################################
# Kāṇḍa Handler
###############################################################################

    def _handle_kanda(
        self,
        line: str,
    ) -> None:
        """
        Handle a Kāṇḍa heading.

        Expected examples
        -----------------

            प्रथमकाण्डः

            स्वर्गादिकाण्डः

            भूमिवर्गकाण्डः

        A new Kāṇḍa always closes the previous structural scope.
        """

        context = self.context

        # ---------------------------------------------------------
        # Validate parser state
        # ---------------------------------------------------------

        self._validate_kanda_transition()

        # ---------------------------------------------------------
        # Construct Kāṇḍa
        # ---------------------------------------------------------

        kanda = self._create_kanda(line)

        # ---------------------------------------------------------
        # Register with the book
        # ---------------------------------------------------------

        self.book.add_kanda(kanda)

        # ---------------------------------------------------------
        # Update parser context
        # ---------------------------------------------------------

        context.current_kanda = kanda

        context.current_varga = None

        context.current_verse = None

        context.transition(
            ParserState.IN_KANDA
        )

        context.increment_kanda()

    ###########################################################################
    # Kāṇḍa Helpers
    ###########################################################################

    def _create_kanda(
        self,
        line: str,
    ) -> Kanda:
        """
        Build a Kāṇḍa object from one heading line.

        Parsing rules are intentionally isolated here so that
        future OCR formats or alternate Amarakośa editions can
        override only this logic.
        """

        number = self._extract_kanda_number(line)

        title = self._extract_kanda_title(line)

        return Kanda(

            number=number,

            title=title,

        )

    ###########################################################################

    def _extract_kanda_number(
        self,
        line: str,
    ) -> int:
        """
        Extract the Kāṇḍa number.

        Current implementation
        ----------------------

        Placeholder implementation.

        Later commits may support

            प्रथम

            द्वितीय

            तृतीय

        Arabic numerals

            1
            2
            3

        Roman numerals

            I
            II
            III

        Returns
        -------
        int
        """

        #
        # Temporary implementation.
        #
        return self.statistics.sections + 1

    ###########################################################################

    def _extract_kanda_title(
        self,
        line: str,
    ) -> str:
        """
        Extract the Kāṇḍa title.

        For now we simply trim whitespace.

        Later this method will normalize

            प्रथमकाण्डः

        into

            प्रथमकाण्ड

        or another canonical form.
        """

        return line.strip()

    ###########################################################################

    def _validate_kanda_transition(
        self,
    ) -> None:
        """
        Validate that a Kāṇḍa may legally appear.

        Future versions may implement stricter ordering
        constraints.

        Raises
        ------
        ValueError
            If an illegal transition is detected.
        """

        state = self.context.state

        if state == ParserState.ERROR:

            raise ValueError(

                "Cannot create Kāṇḍa while parser "

                "is in ERROR state."

            )
#####Siva4

###############################################################################
# Varga Handler
###############################################################################

    def _handle_varga(
        self,
        line: str,
    ) -> None:
        """
        Handle a Varga heading.

        Expected examples
        -----------------

            स्वर्गवर्गः

            व्योमवर्गः

            दिक्वर्गः

        Every Varga belongs to the current Kāṇḍa.
        """

        context = self.context

        # ---------------------------------------------------------
        # Validate parser state
        # ---------------------------------------------------------

        self._validate_varga_transition()

        # ---------------------------------------------------------
        # Ensure a Kāṇḍa exists
        # ---------------------------------------------------------

        if context.current_kanda is None:

            raise ValueError(
                "Encountered Varga before any Kāṇḍa."
            )

        # ---------------------------------------------------------
        # Construct Varga
        # ---------------------------------------------------------

        varga = self._create_varga(line)

        # ---------------------------------------------------------
        # Attach to current Kāṇḍa
        # ---------------------------------------------------------

        context.current_kanda.add_varga(varga)

        # ---------------------------------------------------------
        # Update parser context
        # ---------------------------------------------------------

        context.current_varga = varga

        context.current_verse = None

        context.transition(
            ParserState.IN_VARGA
        )

        context.increment_varga()

    ###########################################################################
    # Varga Helpers
    ###########################################################################

    def _create_varga(
        self,
        line: str,
    ) -> Varga:
        """
        Construct a Varga object.
        """

        return Varga(

            number=self._extract_varga_number(line),

            title=self._extract_varga_title(line),

        )

    ###########################################################################

    def _extract_varga_number(
        self,
        line: str,
    ) -> int:
        """
        Determine the sequential Varga number.

        Current implementation simply assigns
        sequential numbering within the Kāṇḍa.
        """

        kanda = self.context.current_kanda

        if kanda is None:

            return 1

        return len(kanda.vargas) + 1

    ###########################################################################

    def _extract_varga_title(
        self,
        line: str,
    ) -> str:
        """
        Extract the canonical Varga title.

        Later revisions may normalize

            स्वर्गवर्गः

        into

            स्वर्गवर्ग
        """

        return line.strip()

    ###########################################################################

    def _validate_varga_transition(
        self,
    ) -> None:
        """
        Validate parser transition before
        creating a new Varga.
        """

        state = self.context.state

        if state == ParserState.ERROR:

            raise ValueError(
                "Cannot create Varga while parser "
                "is in ERROR state."
            )

        if self.context.current_kanda is None:

            raise ValueError(
                "No active Kāṇḍa exists."
            )

######Siva5            

###############################################################################
# Verse Handler
###############################################################################

    def _handle_verse(
        self,
        line: str,
    ) -> None:
        """
        Handle one Amarakośa verse.

        Expected examples
        -----------------

            स्वर्गो द्यौर्दिवमम्बरम् ।

            ...
        """

        context = self.context

        # ---------------------------------------------------------
        # Validate parser state
        # ---------------------------------------------------------

        self._validate_verse_transition()

        # ---------------------------------------------------------
        # Ensure structural context exists
        # ---------------------------------------------------------

        if context.current_kanda is None:

            raise ValueError(
                "Verse encountered before Kāṇḍa."
            )

        if context.current_varga is None:

            raise ValueError(
                "Verse encountered before Varga."
            )

        # ---------------------------------------------------------
        # Construct Verse object
        # ---------------------------------------------------------

        verse = self._create_verse(line)

        # ---------------------------------------------------------
        # Attach to current Varga
        # ---------------------------------------------------------

        context.current_varga.add_verse(verse)

        # ---------------------------------------------------------
        # Update parser context
        # ---------------------------------------------------------

        context.current_verse = verse

        context.transition(
            ParserState.IN_VERSE
        )

        context.increment_verse()

    ###########################################################################
    # Verse Helpers
    ###########################################################################

    def _create_verse(
        self,
        line: str,
    ) -> Verse:
        """
        Construct one Verse object.

        The parser stores the canonical text exactly as it
        appears after Unicode normalization.

        Lexical analysis is intentionally deferred to the
        importer layer.
        """

        return Verse(

            number=self._extract_verse_number(),

            text=self._normalize_verse_text(line),

        )

    ###########################################################################

    def _extract_verse_number(
        self,
    ) -> int:
        """
        Determine the next verse number.

        Current implementation uses sequential numbering
        within the active Varga.

        Future versions may detect explicit verse numbers
        embedded in the source text.
        """

        varga = self.context.current_varga

        if varga is None:

            return 1

        return len(varga.verses) + 1

    ###########################################################################

    def _normalize_verse_text(
        self,
        line: str,
    ) -> str:
        """
        Normalize one verse.

        Additional normalization rules may later include

            • danda spacing
            • OCR cleanup
            • punctuation normalization
            • zero-width character removal
        """

        return line.strip()

    ###########################################################################

    def _validate_verse_transition(
        self,
    ) -> None:
        """
        Validate parser state before creating a Verse.
        """

        context = self.context

        if context.state == ParserState.ERROR:

            raise ValueError(
                "Cannot create Verse while parser "
                "is in ERROR state."
            )

        if context.current_kanda is None:

            raise ValueError(
                "No active Kāṇḍa."
            )

        if context.current_varga is None:

            raise ValueError(
                "No active Varga."
            )

#####Siva6            

###############################################################################
# Unknown Line Handler
###############################################################################

    def _handle_unknown(
        self,
        line: str,
    ) -> None:
        """
        Handle an unclassified line.

        Unknown lines do not immediately terminate parsing.
        They are recorded as recoverable parser errors.

        Future parser versions may recognise additional
        Amarakośa constructs without changing the main loop.
        """

        context = self.context

        self.statistics.unknown_lines += 1

        context.add_error(

            ImportError(

                line_number=context.line_number,

                message=f"Unrecognized line: {line}",

                severity="warning",

            )

        )

        #
        # Remain in the current parser state.
        #
        # The next recognised structural line should allow the
        # parser to continue normally.
        #

    ###########################################################################
    # Empty Line Handler
    ###########################################################################

    def _handle_empty(
        self,
        line: str,
    ) -> None:
        """
        Ignore blank lines while updating statistics.
        """

        self.statistics.empty_lines += 1

    ###########################################################################
    # Comment Handler
    ###########################################################################

    def _handle_comment(
        self,
        line: str,
    ) -> None:
        """
        Ignore comment lines.

        Typical examples include

            #
            %
            //
            OCR annotations
        """

        self.statistics.comment_lines += 1

    ###########################################################################
    # Validation Helpers
    ###########################################################################

    def _ensure_kanda(self) -> None:
        """
        Ensure an active Kāṇḍa exists.
        """

        if self.context.current_kanda is None:

            raise ValueError(

                "No active Kāṇḍa."

            )

    ###########################################################################

    def _ensure_varga(self) -> None:
        """
        Ensure an active Varga exists.
        """

        self._ensure_kanda()

        if self.context.current_varga is None:

            raise ValueError(

                "No active Varga."

            )

    ###########################################################################

    def _ensure_verse_context(self) -> None:
        """
        Ensure the parser is positioned inside
        a valid Verse context.
        """

        self._ensure_varga()

    ###########################################################################
    # Recovery Helpers
    ###########################################################################

    def _recover(
        self,
        exception: Exception,
    ) -> None:
        """
        Record a recoverable parser error.

        Recovery strategy

        • preserve current parser state

        • record error

        • continue parsing
        """

        self.context.add_error(

            ImportError(

                line_number=self.context.line_number,

                message=str(exception),

                severity="warning",

            )

        )

        self.statistics.recovered_errors += 1

    ###########################################################################

    def _fatal(
        self,
        exception: Exception,
    ) -> None:
        """
        Record a fatal parser error.

        Fatal errors terminate parsing.
        """

        self.context.state = ParserState.ERROR

        self.context.add_error(

            ImportError(

                line_number=self.context.line_number,

                message=str(exception),

                severity="fatal",

            )

        )

        raise exception

    ###########################################################################
    # Safe Dispatcher
    ###########################################################################

    def _safe_dispatch(
        self,
        line_type: LineType,
        line: str,
    ) -> None:
        """
        Execute one parser handler with automatic
        recovery support.
        """

        try:

            self._dispatch(

                line_type,

                line,

            )

        except ValueError as exc:

            #
            # Structural validation errors are considered
            # recoverable unless explicitly escalated.
            #

            self._recover(exc)

        except Exception as exc:

            self._fatal(exc)

######Siva7

###############################################################################
# Object Construction Helpers
###############################################################################

    def _append_kanda(
        self,
        kanda: Kanda,
    ) -> None:
        """
        Append a Kāṇḍa to the Amarakośa.
        """

        self.book.add_kanda(kanda)

        self.context.current_kanda = kanda
        self.context.current_varga = None
        self.context.current_verse = None

    ###########################################################################

    def _append_varga(
        self,
        varga: Varga,
    ) -> None:
        """
        Append a Varga to the active Kāṇḍa.
        """

        self._ensure_kanda()

        self.context.current_kanda.add_varga(varga)

        self.context.current_varga = varga
        self.context.current_verse = None

    ###########################################################################

    def _append_verse(
        self,
        verse: Verse,
    ) -> None:
        """
        Append a Verse to the active Varga.
        """

        self._ensure_varga()

        self.context.current_varga.add_verse(verse)

        self.context.current_verse = verse

    ###########################################################################
    # Factory Helpers
    ###########################################################################

    def _new_kanda(
        self,
        number: int,
        title: str,
    ) -> Kanda:
        """
        Create a canonical Kāṇḍa object.
        """

        return Kanda(
            number=number,
            title=title.strip(),
        )

    ###########################################################################

    def _new_varga(
        self,
        number: int,
        title: str,
    ) -> Varga:
        """
        Create a canonical Varga object.
        """

        return Varga(
            number=number,
            title=title.strip(),
        )

    ###########################################################################

    def _new_verse(
        self,
        number: int,
        text: str,
    ) -> Verse:
        """
        Create a canonical Verse object.
        """

        return Verse(
            number=number,
            text=text.strip(),
        )

    ###########################################################################
    # Registration Helpers
    ###########################################################################

    def _register_kanda(
        self,
        line: str,
    ) -> Kanda:
        """
        Construct and register a Kāṇḍa from one input line.
        """

        kanda = self._new_kanda(
            number=self._extract_kanda_number(line),
            title=self._extract_kanda_title(line),
        )

        self._append_kanda(kanda)

        self.statistics.kandas += 1

        self.context.transition(
            ParserState.IN_KANDA
        )

        return kanda

    ###########################################################################

    def _register_varga(
        self,
        line: str,
    ) -> Varga:
        """
        Construct and register a Varga.
        """

        varga = self._new_varga(
            number=self._extract_varga_number(line),
            title=self._extract_varga_title(line),
        )

        self._append_varga(varga)

        self.statistics.vargas += 1

        self.context.transition(
            ParserState.IN_VARGA
        )

        return varga

    ###########################################################################

    def _register_verse(
        self,
        line: str,
    ) -> Verse:
        """
        Construct and register a Verse.
        """

        verse = self._new_verse(
            number=self._extract_verse_number(),
            text=self._normalize_verse_text(line),
        )

        self._append_verse(verse)

        self.statistics.verses += 1

        self.context.transition(
            ParserState.IN_VERSE
        )

        return verse

#######Siva8        

###############################################################################
# Parser Finalization
###############################################################################

    def _update_statistics(self) -> None:
        """
        Synchronize aggregate import statistics from the
        constructed domain model.

        This provides a final consistency pass after parsing.
        """

        statistics = self.statistics
        book = self.book

        statistics.kandas = len(book.kandas)

        statistics.vargas = sum(
            len(k.vargas)
            for k in book.kandas
        )

        statistics.verses = sum(
            len(v.verses)
            for k in book.kandas
            for v in k.vargas
        )

    ###########################################################################

    def _validate_completion(self) -> None:
        """
        Validate the completed document.

        Raises
        ------
        ValueError
            If the parsed document is structurally invalid.
        """

        if not self.book.kandas:

            raise ValueError(
                "Imported Amarakośa contains no Kāṇḍas."
            )

        for kanda in self.book.kandas:

            if not kanda.vargas:

                self.context.add_error(

                    ImportError(

                        line_number=0,

                        message=(
                            f"Kāṇḍa '{kanda.title}' "
                            "contains no Vargas."
                        ),

                        severity="warning",

                    )

                )

            for varga in kanda.vargas:

                if not varga.verses:

                    self.context.add_error(

                        ImportError(

                            line_number=0,

                            message=(
                                f"Varga '{varga.title}' "
                                "contains no Verses."
                            ),

                            severity="warning",

                        )

                    )

    ###########################################################################

    def _finalize(self) -> ImportResult:
        """
        Complete the parsing operation.

        Returns
        -------
        ImportResult
        """

        self._update_statistics()

        self._validate_completion()

        status = (
            ImportStatus.SUCCESS
            if not self.context.has_fatal_errors
            else ImportStatus.FAILED
        )

        return ImportResult(

            status=status,

            book=self.book,

            statistics=self.statistics,

            errors=tuple(self.context.errors),

        )

###############################################################################
# Utility Methods
###############################################################################

    def reset(self) -> None:
        """
        Reset the parser.

        Configuration is preserved.
        """

        self._context = None

    ###########################################################################

    @property
    def current_state(self) -> ParserState:
        """
        Current parser state.
        """

        return self.context.state

    ###########################################################################

    @property
    def line_number(self) -> int:
        """
        Current input line number.
        """

        return self.context.line_number

    ###########################################################################

    @property
    def error_count(self) -> int:
        """
        Number of parser errors.
        """

        return len(self.context.errors)

    ###########################################################################

    @property
    def warning_count(self) -> int:
        """
        Number of non-fatal warnings.
        """

        return sum(
            1
            for error in self.context.errors
            if error.severity == "warning"
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(self) -> str:

        if self._context is None:

            return (
                "AmarakoshaParser("
                "state=UNINITIALIZED)"
            )

        return (

            "AmarakoshaParser("

            f"state={self.context.state.name}, "

            f"line={self.context.line_number}, "

            f"kandas={self.statistics.kandas}, "

            f"vargas={self.statistics.vargas}, "

            f"verses={self.statistics.verses}, "

            f"errors={self.error_count}"

            ")"

        )

