
from pathlib import Path
import ast
import shutil


TARGET = Path(
    "/content/SanskritAI/acquisition/acquirers/default_source_acquirer.py"
)

BACKUP = TARGET.with_suffix(
    TARGET.suffix + ".bak_13r8f3"
)

IMPORT_LINE = (
    "from SanskritAI.acquisition.downloaders.local_file_importer "
    "import LocalFileImporter"
)


print("=" * 72)
print("13R-8F-3 — Generic local acquisition dispatch repair")
print("=" * 72)


# ------------------------------------------------------------------
# 1. Read production file
# ------------------------------------------------------------------

if not TARGET.is_file():
    raise RuntimeError(
        f"Production target does not exist: {TARGET}"
    )

original = TARGET.read_text(
    encoding="utf-8"
)

print("\nTarget:")
print(TARGET)


# ------------------------------------------------------------------
# 2. Validate original syntax
# ------------------------------------------------------------------

try:
    tree = ast.parse(
        original,
        filename=str(TARGET),
    )
except SyntaxError as exc:
    raise RuntimeError(
        f"Production file contains invalid Python: {exc}"
    )

print("Existing Python syntax: PASS")


# ------------------------------------------------------------------
# 3. Locate DefaultSourceAcquirer.acquire()
# ------------------------------------------------------------------

acquire_node = None

for node in tree.body:

    if not isinstance(
        node,
        ast.ClassDef,
    ):
        continue

    if node.name != "DefaultSourceAcquirer":
        continue

    for child in node.body:

        if isinstance(
            child,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ) and child.name == "acquire":

            acquire_node = child
            break

    break


if acquire_node is None:
    raise RuntimeError(
        "Could not locate "
        "DefaultSourceAcquirer.acquire(). "
        "Production file was NOT modified."
    )


print(
    "Located acquire(): "
    f"lines {acquire_node.lineno}-"
    f"{acquire_node.end_lineno}"
)


# ------------------------------------------------------------------
# 4. Locate _validate_manifest() structurally.
#
# Do NOT search for:
#
#     self._validate_manifest(manifest, result)
#
# because the production implementation is multiline.
# ------------------------------------------------------------------

validation_call = None

for node in ast.walk(acquire_node):

    if not isinstance(
        node,
        ast.Call,
    ):
        continue

    func = node.func

    if (
        isinstance(func, ast.Attribute)
        and func.attr == "_validate_manifest"
    ):
        validation_call = node
        break


if validation_call is None:
    raise RuntimeError(
        "Could not locate the structural "
        "_validate_manifest() call inside acquire(). "
        "Production file was NOT modified."
    )


print(
    "Located _validate_manifest(): "
    f"line {validation_call.lineno}"
)


# ------------------------------------------------------------------
# 5. Verify the disabled-manifest guard occurs BEFORE validation.
#
# This protects the existing contract:
#
#     disabled manifest
#          -> SKIPPED
#          -> successful result
#
# Local dispatch must not bypass this behavior.
# ------------------------------------------------------------------

disabled_guard = None

for node in acquire_node.body:

    if not isinstance(
        node,
        ast.If,
    ):
        continue

    test = node.test

    if (
        isinstance(test, ast.UnaryOp)
        and isinstance(test.op, ast.Not)
        and isinstance(test.operand, ast.Attribute)
        and test.operand.attr == "enabled"
    ):
        value = test.operand.value

        if (
            isinstance(value, ast.Name)
            and value.id == "manifest"
        ):
            disabled_guard = node
            break


if disabled_guard is None:
    raise RuntimeError(
        "Could not locate the existing "
        "'if not manifest.enabled' guard. "
        "Production file was NOT modified."
    )


print(
    "Located disabled-manifest guard: "
    f"lines {disabled_guard.lineno}-"
    f"{disabled_guard.end_lineno}"
)


if disabled_guard.end_lineno >= validation_call.lineno:
    raise RuntimeError(
        "The disabled-manifest guard is not before "
        "_validate_manifest(). Unexpected production "
        "structure. Production file was NOT modified."
    )


print(
    "Disabled-manifest guard precedes validation: PASS"
)


# ------------------------------------------------------------------
# 6. Extract source lines
# ------------------------------------------------------------------

lines = original.splitlines(
    keepends=True
)


# ------------------------------------------------------------------
# 7. Add LocalFileImporter import if missing.
#
# Use AST to locate the final top-level import instead of relying
# on a particular import ordering or formatting.
# ------------------------------------------------------------------

if IMPORT_LINE in original:

    print(
        "LocalFileImporter import already present."
    )

    import_added = False

else:

    last_import_end_line = 0

    for node in tree.body:

        if isinstance(
            node,
            (ast.Import, ast.ImportFrom),
        ):
            last_import_end_line = max(
                last_import_end_line,
                node.end_lineno,
            )

    if last_import_end_line == 0:
        raise RuntimeError(
            "Could not locate a top-level import block. "
            "Production file was NOT modified."
        )

    # Insert immediately after the last import statement.
    #
    # AST line numbers are 1-based.
    insertion_index = last_import_end_line

    lines.insert(
        insertion_index,
        IMPORT_LINE + "\n",
    )

    import_added = True

    print(
        "Added LocalFileImporter import after "
        "the existing top-level import block."
    )


# ------------------------------------------------------------------
# 8. Rebuild source after import insertion.
# ------------------------------------------------------------------

updated = "".join(lines)


# ------------------------------------------------------------------
# 9. Re-parse after import modification.
#
# The validation call's line number may have shifted by one line.
# ------------------------------------------------------------------

try:
    tree_after_import = ast.parse(
        updated,
        filename=str(TARGET),
    )
except SyntaxError as exc:
    raise RuntimeError(
        "Adding the import produced invalid Python: "
        f"{exc}. Production file was NOT modified."
    )


# ------------------------------------------------------------------
# 10. Locate acquire() again after import insertion.
# ------------------------------------------------------------------

acquire_after_import = None

for node in tree_after_import.body:

    if not isinstance(
        node,
        ast.ClassDef,
    ):
        continue

    if node.name != "DefaultSourceAcquirer":
        continue

    for child in node.body:

        if isinstance(
            child,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ) and child.name == "acquire":

            acquire_after_import = child
            break

    break


if acquire_after_import is None:
    raise RuntimeError(
        "Could not relocate acquire() after import insertion. "
        "Production file was NOT modified."
    )


# ------------------------------------------------------------------
# 11. Locate _validate_manifest() again.
# ------------------------------------------------------------------

validation_after_import = None

for node in ast.walk(
    acquire_after_import
):

    if not isinstance(
        node,
        ast.Call,
    ):
        continue

    func = node.func

    if (
        isinstance(func, ast.Attribute)
        and func.attr == "_validate_manifest"
    ):
        validation_after_import = node
        break


if validation_after_import is None:
    raise RuntimeError(
        "Could not relocate _validate_manifest() after "
        "import insertion. Production file was NOT modified."
    )


# ------------------------------------------------------------------
# 12. Check whether delegation already exists.
# ------------------------------------------------------------------

local_support_call = False
local_download_call = False

for node in ast.walk(
    acquire_after_import
):

    if not isinstance(
        node,
        ast.Call,
    ):
        continue

    func = node.func

    if (
        isinstance(func, ast.Attribute)
        and func.attr == "supports"
        and isinstance(func.value, ast.Name)
        and func.value.id == "local_importer"
    ):
        local_support_call = True

    if (
        isinstance(func, ast.Attribute)
        and func.attr == "download"
        and isinstance(func.value, ast.Name)
        and func.value.id == "local_importer"
    ):
        local_download_call = True


if local_support_call and local_download_call:

    print(
        "LocalFileImporter delegation already exists."
    )

    already_present = True

else:

    already_present = False


# ------------------------------------------------------------------
# 13. Insert the generic local dispatch.
#
# IMPORTANT:
#
# It is inserted immediately before the actual multiline
# _validate_manifest() call.
#
# Result:
#
#     if not manifest.enabled:
#         ...
#         return result
#
#     local_importer = LocalFileImporter()
#
#     if local_importer.supports(manifest):
#         return local_importer.download(manifest)
#
#     self._validate_manifest(
#         manifest,
#         result,
#     )
# ------------------------------------------------------------------

if not already_present:

    validation_line_index = (
        validation_after_import.lineno - 1
    )

    validation_line = lines[
        validation_line_index
    ]

    indentation = (
        validation_line[
            : len(validation_line)
            - len(validation_line.lstrip())
        ]
    )

    dispatch_block = (
        indentation
        + "local_importer = LocalFileImporter()\n"
        + "\n"
        + indentation
        + "if local_importer.supports(manifest):\n"
        + indentation
        + "    return local_importer.download(manifest)\n"
        + "\n"
    )

    lines.insert(
        validation_line_index,
        dispatch_block,
    )

    updated = "".join(lines)

    print(
        "Inserted generic LocalFileImporter delegation "
        "before _validate_manifest()."
    )

else:

    print(
        "No duplicate delegation inserted."
    )


# ------------------------------------------------------------------
# 14. Validate final Python syntax BEFORE writing.
# ------------------------------------------------------------------

try:
    final_tree = ast.parse(
        updated,
        filename=str(TARGET),
    )
except SyntaxError as exc:
    raise RuntimeError(
        "Final proposed production file contains invalid "
        f"Python: {exc}. Production file was NOT modified."
    )


print(
    "Modified Python syntax: PASS"
)


# ------------------------------------------------------------------
# 15. Locate final acquire() and validate ordering.
# ------------------------------------------------------------------

final_acquire = None

for node in final_tree.body:

    if not isinstance(
        node,
        ast.ClassDef,
    ):
        continue

    if node.name != "DefaultSourceAcquirer":
        continue

    for child in node.body:

        if isinstance(
            child,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ) and child.name == "acquire":

            final_acquire = child
            break

    break


if final_acquire is None:
    raise RuntimeError(
        "Final acquire() could not be located. "
        "Production file was NOT modified."
    )


final_validation = None
final_support = None
final_download = None

for node in ast.walk(
    final_acquire
):

    if not isinstance(
        node,
        ast.Call,
    ):
        continue

    func = node.func

    if (
        isinstance(func, ast.Attribute)
        and func.attr == "_validate_manifest"
    ):
        final_validation = node

    elif (
        isinstance(func, ast.Attribute)
        and func.attr == "supports"
        and isinstance(func.value, ast.Name)
        and func.value.id == "local_importer"
    ):
        final_support = node

    elif (
        isinstance(func, ast.Attribute)
        and func.attr == "download"
        and isinstance(func.value, ast.Name)
        and func.value.id == "local_importer"
    ):
        final_download = node


if final_support is None:
    raise RuntimeError(
        "Final LocalFileImporter.supports() call was not found."
    )


if final_download is None:
    raise RuntimeError(
        "Final LocalFileImporter.download() call was not found."
    )


if final_validation is None:
    raise RuntimeError(
        "Final _validate_manifest() call was not found."
    )


assert (
    final_support.lineno
    < final_validation.lineno
)

assert (
    final_download.lineno
    < final_validation.lineno
)


print(
    "Local dispatch occurs before manifest validation: PASS"
)


# ------------------------------------------------------------------
# 16. Verify the disabled guard remains before local dispatch.
# ------------------------------------------------------------------

final_disabled_guard = None

for node in final_acquire.body:

    if not isinstance(
        node,
        ast.If,
    ):
        continue

    test = node.test

    if (
        isinstance(test, ast.UnaryOp)
        and isinstance(test.op, ast.Not)
        and isinstance(test.operand, ast.Attribute)
        and test.operand.attr == "enabled"
        and isinstance(test.operand.value, ast.Name)
        and test.operand.value.id == "manifest"
    ):
        final_disabled_guard = node
        break


if final_disabled_guard is None:
    raise RuntimeError(
        "Final disabled-manifest guard disappeared."
    )


assert (
    final_disabled_guard.end_lineno
    < final_support.lineno
)

print(
    "Disabled-manifest guard remains before local dispatch: PASS"
)


# ------------------------------------------------------------------
# 17. Create a production backup.
# ------------------------------------------------------------------

if not BACKUP.exists():

    shutil.copy2(
        TARGET,
        BACKUP,
    )

    print(
        "\nProduction backup created:"
    )
    print(
        " ",
        BACKUP,
    )

else:

    print(
        "\nProduction backup already exists:"
    )
    print(
        " ",
        BACKUP,
    )


# ------------------------------------------------------------------
# 18. Write production file.
# ------------------------------------------------------------------

TARGET.write_text(
    updated,
    encoding="utf-8",
)

print(
    "\nProduction file updated:"
)
print(
    TARGET
)


# ------------------------------------------------------------------
# 19. Read back and verify the actual written file.
# ------------------------------------------------------------------

written = TARGET.read_text(
    encoding="utf-8"
)

try:
    written_tree = ast.parse(
        written,
        filename=str(TARGET),
    )
except SyntaxError as exc:
    raise RuntimeError(
        "Written production file contains invalid Python: "
        f"{exc}"
    )


print(
    "Written-file Python syntax: PASS"
)


# ------------------------------------------------------------------
# 20. Final textual sanity checks.
# ------------------------------------------------------------------

assert (
    "LocalFileImporter"
    in written
)

assert (
    "local_importer.supports(manifest)"
    in written
)

assert (
    "local_importer.download(manifest)"
    in written
)

print(
    "Written-file delegation checks: PASS"
)


print("\n" + "=" * 72)
print("13R-8F-3 COMPLETE")
print("=" * 72)

print(
    "\nGeneric acquisition boundary repaired:"
)

print(
    "  local manifest"
    " -> LocalFileImporter"
    " -> AcquisitionResult"
)

print(
    "\nExisting remote acquisition path remains unchanged."
)

print(
    "\nDisabled-manifest behavior remains unchanged."
)

print(
    "\nNo Amarakośa-specific acquirer/downloader class was created."
)

print(
    "\nProduction backup:"
)

print(
    " ",
    BACKUP,
)

print("=" * 72)
