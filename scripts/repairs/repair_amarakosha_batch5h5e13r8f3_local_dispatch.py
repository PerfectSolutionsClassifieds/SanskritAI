
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


# ----------------------------------------------------------------------
# Preconditions
# ----------------------------------------------------------------------

if not TARGET.is_file():
    raise RuntimeError(
        f"Production target does not exist: {TARGET}"
    )


original = TARGET.read_text(
    encoding="utf-8"
)


print("\nTarget:")
print(TARGET)


# ----------------------------------------------------------------------
# Parse existing production file
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# Locate DefaultSourceAcquirer.acquire()
# ----------------------------------------------------------------------

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
        if (
            isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and child.name == "acquire"
        ):
            acquire_node = child
            break

    break


if acquire_node is None:
    raise RuntimeError(
        "Could not locate DefaultSourceAcquirer.acquire(). "
        "Production file was NOT modified."
    )


print(
    "Located acquire(): "
    f"lines {acquire_node.lineno}-"
    f"{acquire_node.end_lineno}"
)


# ----------------------------------------------------------------------
# Locate _validate_manifest() structurally
#
# IMPORTANT:
# The production call is:
#
#     self._validate_manifest(
#         manifest,
#         result,
#     )
#
# It may be nested inside try/if blocks, so ast.walk() is required.
# ----------------------------------------------------------------------

validation_call = None

for node in ast.walk(
    acquire_node
):
    if not isinstance(
        node,
        ast.Call,
    ):
        continue

    func = node.func

    if (
        isinstance(
            func,
            ast.Attribute,
        )
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


# ----------------------------------------------------------------------
# Locate disabled-manifest guard structurally
#
# IMPORTANT:
# The guard is nested inside acquire() -> try -> if.
# Therefore acquire_node.body is NOT sufficient.
# ast.walk(acquire_node) is required.
# ----------------------------------------------------------------------

disabled_guard = None

for node in ast.walk(
    acquire_node
):
    if not isinstance(
        node,
        ast.If,
    ):
        continue

    test = node.test

    # Expected form:
    #
    #     if not manifest.enabled:
    #
    if not (
        isinstance(
            test,
            ast.UnaryOp,
        )
        and isinstance(
            test.op,
            ast.Not,
        )
        and isinstance(
            test.operand,
            ast.Attribute,
        )
        and test.operand.attr == "enabled"
        and isinstance(
            test.operand.value,
            ast.Name,
        )
        and test.operand.value.id == "manifest"
    ):
        continue

    disabled_guard = node
    break


if disabled_guard is None:
    raise RuntimeError(
        "Could not locate the existing "
        "'if not manifest.enabled' guard anywhere "
        "inside acquire(). "
        "Production file was NOT modified."
    )


print(
    "Located disabled-manifest guard: "
    f"lines {disabled_guard.lineno}-"
    f"{disabled_guard.end_lineno}"
)


# ----------------------------------------------------------------------
# Verify disabled guard precedes validation
# ----------------------------------------------------------------------

if (
    disabled_guard.end_lineno
    >= validation_call.lineno
):
    raise RuntimeError(
        "The disabled-manifest guard does not precede "
        "_validate_manifest(). Unexpected production "
        "structure. Production file was NOT modified."
    )


print(
    "Disabled-manifest guard precedes validation: PASS"
)


# ----------------------------------------------------------------------
# Prepare source lines
# ----------------------------------------------------------------------

lines = original.splitlines(
    keepends=True
)


# ----------------------------------------------------------------------
# Add LocalFileImporter import if absent
# ----------------------------------------------------------------------

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
            (
                ast.Import,
                ast.ImportFrom,
            ),
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


# ----------------------------------------------------------------------
# Rebuild after possible import insertion
# ----------------------------------------------------------------------

updated = "".join(lines)


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


# ----------------------------------------------------------------------
# Relocate acquire() after import insertion
# ----------------------------------------------------------------------

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

        if (
            isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and child.name == "acquire"
        ):
            acquire_after_import = child
            break

    break


if acquire_after_import is None:
    raise RuntimeError(
        "Could not relocate acquire() after import insertion. "
        "Production file was NOT modified."
    )


# ----------------------------------------------------------------------
# Relocate validation call after import insertion
# ----------------------------------------------------------------------

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
        isinstance(
            func,
            ast.Attribute,
        )
        and func.attr == "_validate_manifest"
    ):
        validation_after_import = node
        break


if validation_after_import is None:
    raise RuntimeError(
        "Could not relocate _validate_manifest() after "
        "import insertion. Production file was NOT modified."
    )


print(
    "Post-import structural validation: PASS"
)


# ----------------------------------------------------------------------
# Check whether local delegation already exists
# ----------------------------------------------------------------------

local_support_call = None
local_download_call = None

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
        isinstance(
            func,
            ast.Attribute,
        )
        and func.attr == "supports"
        and isinstance(
            func.value,
            ast.Name,
        )
        and func.value.id == "local_importer"
    ):
        local_support_call = node

    if (
        isinstance(
            func,
            ast.Attribute,
        )
        and func.attr == "download"
        and isinstance(
            func.value,
            ast.Name,
        )
        and func.value.id == "local_importer"
    ):
        local_download_call = node


already_present = (
    local_support_call is not None
    and local_download_call is not None
)


if already_present:

    print(
        "LocalFileImporter delegation already exists."
    )

else:

    # --------------------------------------------------------------
    # Insert immediately before _validate_manifest()
    # --------------------------------------------------------------

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


# ----------------------------------------------------------------------
# Final AST validation
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# Locate final acquire()
# ----------------------------------------------------------------------

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

        if (
            isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and child.name == "acquire"
        ):
            final_acquire = child
            break

    break


if final_acquire is None:
    raise RuntimeError(
        "Final acquire() could not be located. "
        "Production file was NOT modified."
    )


# ----------------------------------------------------------------------
# Locate final structural calls
# ----------------------------------------------------------------------

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
        isinstance(
            func,
            ast.Attribute,
        )
        and func.attr == "_validate_manifest"
    ):
        final_validation = node

    elif (
        isinstance(
            func,
            ast.Attribute,
        )
        and func.attr == "supports"
        and isinstance(
            func.value,
            ast.Name,
        )
        and func.value.id == "local_importer"
    ):
        final_support = node

    elif (
        isinstance(
            func,
            ast.Attribute,
        )
        and func.attr == "download"
        and isinstance(
            func.value,
            ast.Name,
        )
        and func.value.id == "local_importer"
    ):
        final_download = node


if final_support is None:
    raise RuntimeError(
        "Final LocalFileImporter.supports() call "
        "was not found."
    )


if final_download is None:
    raise RuntimeError(
        "Final LocalFileImporter.download() call "
        "was not found."
    )


if final_validation is None:
    raise RuntimeError(
        "Final _validate_manifest() call "
        "was not found."
    )


# ----------------------------------------------------------------------
# Verify ordering
# ----------------------------------------------------------------------

if not (
    final_support.lineno
    < final_validation.lineno
):
    raise RuntimeError(
        "LocalFileImporter.supports() does not occur "
        "before _validate_manifest()."
    )


if not (
    final_download.lineno
    < final_validation.lineno
):
    raise RuntimeError(
        "LocalFileImporter.download() does not occur "
        "before _validate_manifest()."
    )


print(
    "Local dispatch occurs before manifest validation: PASS"
)


# ----------------------------------------------------------------------
# Locate final disabled-manifest guard
#
# Again use ast.walk() because it is nested inside try.
# ----------------------------------------------------------------------

final_disabled_guard = None

for node in ast.walk(
    final_acquire
):

    if not isinstance(
        node,
        ast.If,
    ):
        continue

    test = node.test

    if (
        isinstance(
            test,
            ast.UnaryOp,
        )
        and isinstance(
            test.op,
            ast.Not,
        )
        and isinstance(
            test.operand,
            ast.Attribute,
        )
        and test.operand.attr == "enabled"
        and isinstance(
            test.operand.value,
            ast.Name,
        )
        and test.operand.value.id == "manifest"
    ):
        final_disabled_guard = node
        break


if final_disabled_guard is None:
    raise RuntimeError(
        "Final disabled-manifest guard disappeared."
    )


if not (
    final_disabled_guard.end_lineno
    < final_support.lineno
):
    raise RuntimeError(
        "Local dispatch was inserted before the "
        "disabled-manifest guard. This would alter "
        "disabled-manifest semantics."
    )


print(
    "Disabled-manifest guard remains before "
    "local dispatch: PASS"
)


# ----------------------------------------------------------------------
# Verify dispatch is inside acquire() and not outside it
# ----------------------------------------------------------------------

if not (
    final_support.lineno
    >= final_acquire.lineno
    and final_download.lineno
    <= final_acquire.end_lineno
):
    raise RuntimeError(
        "Local dispatch is not contained inside acquire()."
    )


print(
    "Local dispatch containment inside acquire(): PASS"
)


# ----------------------------------------------------------------------
# Create backup immediately before production write
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# Write production file
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# Read-back verification
# ----------------------------------------------------------------------

written = TARGET.read_text(
    encoding="utf-8"
)


try:
    ast.parse(
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


if "LocalFileImporter" not in written:
    raise RuntimeError(
        "Written file does not contain LocalFileImporter."
    )


if "local_importer.supports(manifest)" not in written:
    raise RuntimeError(
        "Written file does not contain "
        "local_importer.supports(manifest)."
    )


if "local_importer.download(manifest)" not in written:
    raise RuntimeError(
        "Written file does not contain "
        "local_importer.download(manifest)."
    )


print(
    "Written-file delegation checks: PASS"
)


# ----------------------------------------------------------------------
# Final report
# ----------------------------------------------------------------------

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
