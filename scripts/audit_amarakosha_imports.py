from pathlib import Path

ROOT = Path("/content/SanskritAI/services/importers")

TARGETS = [
    "amarakosha_parser.py",
    "amarakosha_importer.py",
    "parser_context.py",
    "parser_state.py",
    "parser_validator.py",
    "parser_errors.py",
    "line_classifier.py",
    "unicode_normalizer.py",
    "structure_numbering.py",
    "classification_result.py",
    "amarakosha_builder.py",
    "import_result_builder.py",
]

print("=" * 72)
print("AMARAKOSHA IMPORT-BOUNDARY AUDIT")
print("=" * 72)

for name in TARGETS:

    path = ROOT / name

    print()
    print("-" * 72)
    print(name)
    print("-" * 72)

    if not path.exists():
        print("MISSING")
        continue

    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        stripped = line.strip()

        if (
            stripped.startswith("import ")
            or stripped.startswith("from ")
        ):
            print(
                f"{number:4}: {stripped}"
            )

print()
print("=" * 72)
print("AUDIT COMPLETE")
print("=" * 72)
