
from __future__ import annotations

import inspect
import sys
from pathlib import Path


ROOT = Path("/content/SanskritAI")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def show_object(label, obj):

    print()
    print("=" * 90)
    print(label)
    print("=" * 90)

    print(
        "TYPE:",
        type(obj),
    )

    print(
        "CLASS:",
        type(obj).__module__,
        type(obj).__name__,
    )

    print(
        "REPR:",
        repr(obj),
    )

    if hasattr(obj, "__dict__"):

        print()
        print("__DICT__:")

        for key, value in obj.__dict__.items():

            print(
                f"  {key} = {value!r}"
            )

    print()


def show_signature(label, obj):

    print(
        f"{label}:"
    )

    try:
        print(
            inspect.signature(obj)
        )
    except Exception as exc:
        print(
            f"  <signature unavailable: {exc!r}>"
        )


def main():

    print("=" * 90)
    print("BATCH 4E — AMARAKOSHA RUNTIME DATA-FLOW PROBE")
    print("=" * 90)

    # ---------------------------------------------------------------
    # Imports
    # ---------------------------------------------------------------

    from SanskritAI.amarakosha.parsers.amarakosha_parser import (
        AmarakoshaParser,
    )

    from SanskritAI.amarakosha.importers.amarakosha_importer import (
        AmarakoshaImporter,
    )

    from SanskritAI.amarakosha.registries.amarakosha_registry import (
        AmarakoshaRegistry,
    )

    from SanskritAI.amarakosha.builders.synset_builder import (
        SynsetBuilder,
    )

    from SanskritAI.amarakosha.builders.varga_builder import (
        VargaBuilder,
    )

    from SanskritAI.amarakosha.records.synset_record import (
        SynsetRecord,
    )

    from SanskritAI.amarakosha.records.varga_record import (
        VargaRecord,
    )

    # ---------------------------------------------------------------
    # Class signatures
    # ---------------------------------------------------------------

    print()
    print("CLASS / METHOD SIGNATURES")
    print("-" * 90)

    for label, obj in [
        ("AmarakoshaParser", AmarakoshaParser),
        ("AmarakoshaImporter", AmarakoshaImporter),
        ("AmarakoshaRegistry", AmarakoshaRegistry),
        ("SynsetBuilder", SynsetBuilder),
        ("VargaBuilder", VargaBuilder),
        ("SynsetRecord", SynsetRecord),
        ("VargaRecord", VargaRecord),
    ]:

        print()
        print(label)

        try:
            print(
                "  constructor:",
                inspect.signature(obj),
            )
        except Exception as exc:
            print(
                "  constructor unavailable:",
                repr(exc),
            )

        for method_name in (
            "__init__",
            "parse",
            "parse_kanda",
            "parse_varga",
            "parse_synset",
            "import_source",
            "register",
            "register_many",
            "vargas",
            "synsets",
            "build",
            "add_lexeme",
            "add_synset",
        ):

            if hasattr(obj, method_name):

                method = getattr(
                    obj,
                    method_name,
                )

                show_signature(
                    f"  {method_name}",
                    method,
                )

    # ---------------------------------------------------------------
    # Instantiate registry
    # ---------------------------------------------------------------

    print()
    print("=" * 90)
    print("REGISTRY RUNTIME")
    print("=" * 90)

    registry = AmarakoshaRegistry()

    show_object(
        "Fresh AmarakoshaRegistry",
        registry,
    )

    # ---------------------------------------------------------------
    # Instantiate parser
    # ---------------------------------------------------------------

    print()
    print("=" * 90)
    print("PARSER RUNTIME")
    print("=" * 90)

    try:

        parser = AmarakoshaParser(
            registry=registry
        )

        show_object(
            "AmarakoshaParser(registry=registry)",
            parser,
        )

    except Exception as exc:

        print(
            "Parser construction failed:",
            repr(exc),
        )

        try:

            parser = AmarakoshaParser()

            show_object(
                "AmarakoshaParser()",
                parser,
            )

        except Exception as exc2:

            print(
                "Parser() also failed:",
                repr(exc2),
            )

            parser = None

    # ---------------------------------------------------------------
    # Instantiate importer
    # ---------------------------------------------------------------

    print()
    print("=" * 90)
    print("IMPORTER RUNTIME")
    print("=" * 90)

    try:

        importer = AmarakoshaImporter()

        show_object(
            "AmarakoshaImporter()",
            importer,
        )

    except Exception as exc:

        print(
            "Importer construction failed:",
            repr(exc),
        )

        importer = None

    # ---------------------------------------------------------------
    # Registry API
    # ---------------------------------------------------------------

    print()
    print("=" * 90)
    print("REGISTRY API")
    print("=" * 90)

    for method_name in (
        "vargas",
        "synsets",
    ):

        if hasattr(
            registry,
            method_name,
        ):

            try:

                value = getattr(
                    registry,
                    method_name,
                )()

                print(
                    f"{method_name}() -> "
                    f"{type(value)} "
                    f"{value!r}"
                )

            except Exception as exc:

                print(
                    f"{method_name}() FAILED -> "
                    f"{exc!r}"
                )

    # ---------------------------------------------------------------
    # Empty-source parser probe
    # ---------------------------------------------------------------

    if parser is not None:

        print()
        print("=" * 90)
        print("EMPTY SOURCE PARSER PROBE")
        print("=" * 90)

        for source in (
            "",
            [],
            "",
        ):

            try:

                result = parser.parse(
                    source
                )

                print()
                print(
                    f"parse({source!r})"
                    f" -> {result!r}"
                )

            except Exception as exc:

                print()
                print(
                    f"parse({source!r})"
                    f" FAILED -> {exc!r}"
                )

    # ---------------------------------------------------------------
    # Existing registry state after probe
    # ---------------------------------------------------------------

    print()
    print("=" * 90)
    print("REGISTRY STATE AFTER PARSER PROBE")
    print("=" * 90)

    show_object(
        "Registry after probe",
        registry,
    )

    try:

        print(
            "vargas():",
            registry.vargas(),
        )

    except Exception as exc:

        print(
            "vargas() failed:",
            repr(exc),
        )

    try:

        print(
            "synsets():",
            registry.synsets(),
        )

    except Exception as exc:

        print(
            "synsets() failed:",
            repr(exc),
        )

    print()
    print("=" * 90)
    print("BATCH 4E COMPLETE")
    print("=" * 90)
    print()
    print(
        "This probe is diagnostic only."
    )
    print(
        "No production code was modified."
    )


if __name__ == "__main__":
    main()
