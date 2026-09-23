
from pathlib import Path
import ast
import shutil
import sys


TARGET = Path(
    "/content/SanskritAI/acquisition/acquirers/default_source_acquirer.py"
)

print("=" * 72)
print("13R-8F-3 — Generic local acquisition dispatch repair")
print("=" * 72)

if not TARGET.is_file():
    raise RuntimeError(
        f"Production target does not exist: {TARGET}"
    )

original = TARGET.read_text(encoding="utf-8")

print("\nTarget:")
print(TARGET)

# ------------------------------------------------------------------
# 1. Verify the production file is valid Python BEFORE modifying it.
# ------------------------------------------------------------------

try:
    ast.parse(original)
except SyntaxError as exc:
    raise RuntimeError(
        f"Production file is not valid Python: {exc}"
    )

print("Existing Python syntax: PASS")


# ------------------------------------------------------------------
# 2. Do not duplicate the import.
# ------------------------------------------------------------------

IMPORT_LINE = (
    "from SanskritAI.acquisition.downloaders.local_file_importer "
    "import LocalFileImporter"
)

if IMPORT_LINE in original:
    print("LocalFileImporter import already present.")
    import_added = False

else:
    # --------------------------------------------------------------
    # Find the last top-level import statement.
    #
    # This avoids depending on a particular existing import order
    # or line wrapping.
    # --------------------------------------------------------------

    lines = original.splitlines(keepends=True)

    tree = ast.parse(original)

    import_end_line = 0

    for node in tree.body:
        if isinstance(
            node,
            (ast.Import, ast.ImportFrom),
        ):
            import_end_line = max(
                import_end_line,
                node.end_lineno or node.lineno,
            )

    if import_end_line == 0:
        raise RuntimeError(
            "Could not locate a top-level import section. "
            "Production file was not modified."
        )

    insertion_index = import_end_line

    lines.insert(
        insertion_index,
        IMPORT_LINE + "\n",
    )

    updated = "".join(lines)

    original = updated

    print(
        "Added LocalFileImporter import after the existing "
        "top-level import block."
    )

    import_added = True


# ------------------------------------------------------------------
# 3. Locate the acquire() method.
# ------------------------------------------------------------------

tree = ast.parse(original)

acquire_node = None

for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if node.name == "acquire":
            acquire_node = node
            break

if acquire_node is None:
    raise RuntimeError(
        "Could not locate DefaultSourceAcquirer.acquire(). "
        "Production file was not modified."
    )

print(
    "Located acquire(): "
    f"lines {acquire_node.lineno}-{acquire_node.end_lineno}"
)


# ------------------------------------------------------------------
# 4. Locate the existing manifest-enabled guard.
#
# We deliberately keep:
#
#     if not manifest.enabled:
#         ...
#         return result
#
# BEFORE local dispatch.
#
# Disabled manifests must remain disabled regardless of source type.
# ------------------------------------------------------------------

acquire_source = ast.get_source_segment(
    original,
    acquire_node,
)

if acquire_source is None:
    raise RuntimeError(
        "Could not extract acquire() source. "
        "Production file was not modified."
    )


# ------------------------------------------------------------------
# 5. Check whether local dispatch is already present.
# ------------------------------------------------------------------

if (
    "LocalFileImporter()" in acquire_source
    and "local_importer.supports(manifest)" in acquire_source
):
    print(
        "LocalFileImporter delegation already exists "
        "inside acquire()."
    )

    already_present = True

else:
    already_present = False


# ------------------------------------------------------------------
# 6. Identify the first validation call.
#
# Current architecture has:
#
#     self._validate_manifest(manifest, result)
#
# The local dispatch belongs immediately before that validation,
# but AFTER the enabled-manifest guard.
# ------------------------------------------------------------------

VALIDATION_TEXT = (
    "self._validate_manifest(manifest, result)"
)

validation_position = acquire_source.find(
    VALIDATION_TEXT
)

if validation_position == -1:
    raise RuntimeError(
        "Could not locate the expected "
        "_validate_manifest(manifest, result) call "
        "inside acquire(). "
        "Production file was not modified."
    )


# ------------------------------------------------------------------
# 7. Find the exact source text immediately before validation.
#
# We expect the existing code to have already performed:
#
#     if not manifest.enabled:
#         ...
#         return result
#
# We do not rewrite that block.
# ------------------------------------------------------------------

if not already_present:

    dispatch_block = """        local_importer = LocalFileImporter()

        if local_importer.supports(manifest):
            return local_importer.download(manifest)

"""

    updated_acquire_source = (
        acquire_source[:validation_position]
        + dispatch_block
        + acquire_source[validation_position:]
    )

    # --------------------------------------------------------------
    # Replace only the acquire() method body/source.
    #
    # Use the original line boundaries from the AST.
    # --------------------------------------------------------------

    all_lines = original.splitlines(keepends=True)

    start_index = acquire_node.lineno - 1
    end_index = acquire_node.end_lineno

    old_method_text = "".join(
        all_lines[start_index:end_index]
    )

    if old_method_text != acquire_source:
        raise RuntimeError(
            "The extracted acquire() source does not match "
            "the source file line range. "
            "Production file was not modified."
        )

    all_lines[start_index:end_index] = [
        updated_acquire_source
    ]

    updated = "".join(all_lines)

    print(
        "Inserted generic LocalFileImporter delegation "
        "before _validate_manifest()."
    )

else:
    updated = original


# ------------------------------------------------------------------
# 8. Validate the resulting source BEFORE writing it.
# ------------------------------------------------------------------

try:
    ast.parse(updated)
except SyntaxError as exc:
    raise RuntimeError(
        "The proposed production modification produced invalid "
        f"Python: {exc}. Production file was NOT written."
    )

print("Modified Python syntax: PASS")


# ------------------------------------------------------------------
# 9. Verify the intended delegation exists in the final source.
# ------------------------------------------------------------------

if (
    "LocalFileImporter" not in updated
    or "local_importer.supports(manifest)" not in updated
    or "local_importer.download(manifest)" not in updated
):
    raise RuntimeError(
        "Final source does not contain the expected generic "
        "local-dispatch delegation. Production file was NOT written."
    )

print("Delegation presence check: PASS")


# ------------------------------------------------------------------
# 10. Verify the delegation is located BEFORE validation.
# ------------------------------------------------------------------

dispatch_position = updated.find(
    "local_importer.supports(manifest)"
)

validation_position_final = updated.find(
    "self._validate_manifest(manifest, result)"
)

if dispatch_position == -1:
    raise RuntimeError(
        "Could not locate local dispatch in final source."
    )

if validation_position_final == -1:
    raise RuntimeError(
        "Could not locate manifest validation in final source."
    )

if dispatch_position >= validation_position_final:
    raise RuntimeError(
        "Local dispatch is not before manifest validation. "
        "Production file was NOT written."
    )

print(
    "Local dispatch occurs before URL validation: PASS"
)


# ------------------------------------------------------------------
# 11. Backup current production file before writing.
# ------------------------------------------------------------------

backup = TARGET.with_suffix(
    TARGET.suffix + ".bak_13r8f3"
)

if not backup.exists():
    shutil.copy2(TARGET, backup)
    print("Production backup created:")
    print(" ", backup)
else:
    print("Production backup already exists:")
    print(" ", backup)


# ------------------------------------------------------------------
# 12. Write production modification.
# ------------------------------------------------------------------

TARGET.write_text(
    updated,
    encoding="utf-8",
)

print("\nProduction file updated:")
print(TARGET)


# ------------------------------------------------------------------
# 13. Final verification from disk.
# ------------------------------------------------------------------

written = TARGET.read_text(
    encoding="utf-8"
)

try:
    ast.parse(written)
except SyntaxError as exc:
    raise RuntimeError(
        f"Written production file is invalid Python: {exc}"
    )

assert (
    "local_importer.supports(manifest)"
    in written
)

assert (
    "local_importer.download(manifest)"
    in written
)

assert (
    written.find(
        "local_importer.supports(manifest)"
    )
    <
    written.find(
        "self._validate_manifest(manifest, result)"
    )
)

print("Written-file syntax: PASS")
print("Written-file delegation: PASS")
print("Written-file ordering: PASS")


print("\n" + "=" * 72)
print("13R-8F-3 COMPLETE")
print("=" * 72)

if already_present:
    print(
        "No duplicate local-dispatch block was inserted."
    )
else:
    print(
        "Generic local acquisition delegation was inserted."
    )

print(
    "\nArchitecture preserved:"
)

print(
    "  Local manifest"
    " -> LocalFileImporter"
    " -> AcquisitionResult"
)

print(
    "  Remote manifest"
    " -> existing DefaultSourceAcquirer path"
)

print(
    "\nNo Amarakośa-specific acquisition class was created."
)

print("=" * 72)
