
from pathlib import Path

TARGET = Path(
    "/content/SanskritAI/acquisition/acquirers/default_source_acquirer.py"
)

text = TARGET.read_text(encoding="utf-8")

print("=" * 72)
print("13R-8F-3 — Generic local acquisition dispatch repair")
print("=" * 72)

# ------------------------------------------------------------------
# 1. Add LocalFileImporter import.
# ------------------------------------------------------------------

IMPORT_ANCHOR = (
    "from SanskritAI.acquisition.models.acquisition_result "
    "import AcquisitionResult\n"
)

IMPORT_LINE = (
    "from SanskritAI.acquisition.downloaders.local_file_importer "
    "import LocalFileImporter\n"
)

if IMPORT_LINE not in text:
    if IMPORT_ANCHOR not in text:
        raise RuntimeError(
            "Expected AcquisitionResult import anchor was not found. "
            "Production file may have changed."
        )

    text = text.replace(
        IMPORT_ANCHOR,
        IMPORT_ANCHOR + IMPORT_LINE,
        1,
    )

    print("Added LocalFileImporter import.")
else:
    print("LocalFileImporter import already present.")

# ------------------------------------------------------------------
# 2. Insert generic local dispatch before manifest validation.
# ------------------------------------------------------------------

OLD = """        result = AcquisitionResult(source=manifest.source)
        try:
            if not manifest.enabled:
"""

NEW = """        result = AcquisitionResult(source=manifest.source)
        try:
            local_importer = LocalFileImporter()

            if local_importer.supports(manifest):
                return local_importer.download(manifest)

            if not manifest.enabled:
"""

if OLD not in text:
    raise RuntimeError(
        "Expected acquire() insertion anchor was not found. "
        "No production modification was written."
    )

if "local_importer = LocalFileImporter()" not in text:
    text = text.replace(
        OLD,
        NEW,
        1,
    )

    print("Inserted generic local dispatch.")
else:
    print(
        "LocalFileImporter delegation already exists; "
        "no duplicate dispatch inserted."
    )

# ------------------------------------------------------------------
# 3. Write only after all assertions succeed.
# ------------------------------------------------------------------

TARGET.write_text(text, encoding="utf-8")

print("\nProduction file updated:")
print(TARGET)

print("\nRepair:")
print(
    "DefaultSourceAcquirer now delegates manifests carrying "
    "'source_path' metadata to LocalFileImporter before URL "
    "validation."
)

print("\n" + "=" * 72)
print("13R-8F-3 COMPLETE")
print("=" * 72)
