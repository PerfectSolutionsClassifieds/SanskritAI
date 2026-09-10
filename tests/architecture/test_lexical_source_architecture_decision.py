from __future__ import annotations

import ast
from pathlib import Path


REPO_ROOT = Path("/content/SanskritAI")

DOMAIN_SOURCE = (
    REPO_ROOT / "domain" / "lexical" / "lexical_source.py"
)

KERNEL_SOURCE = (
    REPO_ROOT / "lexical" / "models" / "lexical_source.py"
)


def _module_name(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT)
    return ".".join(relative.with_suffix("").parts)


def _imports_from(path: Path) -> list[str]:
    tree = ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )

    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def test_both_lexical_source_definitions_exist():
    assert DOMAIN_SOURCE.exists(), (
        "Domain LexicalSource definition is missing."
    )

    assert KERNEL_SOURCE.exists(), (
        "Kernel LexicalSource definition is missing."
    )


def test_domain_and_kernel_lexical_source_are_separate_modules():
    assert _module_name(DOMAIN_SOURCE) == (
        "domain.lexical.lexical_source"
    )

    assert _module_name(KERNEL_SOURCE) == (
        "lexical.models.lexical_source"
    )


def test_domain_lexical_source_does_not_import_kernel_lexical_source():
    imports = _imports_from(DOMAIN_SOURCE)

    forbidden = "lexical.models.lexical_source"

    assert forbidden not in imports, (
        "Domain LexicalSource must remain independent of the "
        "kernel LexicalSource."
    )


def test_kernel_lexical_source_does_not_import_domain_lexical_source():
    imports = _imports_from(KERNEL_SOURCE)

    forbidden = "domain.lexical.lexical_source"

    assert forbidden not in imports, (
        "Kernel LexicalSource must remain independent of the "
        "domain LexicalSource."
    )


def test_architecture_does_not_require_a_lexical_source_mapper_yet():
    """
    Architectural decision:

        RETAIN BOTH

    No Domain LexicalSource -> Kernel LexicalSource mapping
    is currently required by production architecture.

    This test intentionally does not require an adapter/mapper.
    """

    domain_text = DOMAIN_SOURCE.read_text(encoding="utf-8")
    kernel_text = KERNEL_SOURCE.read_text(encoding="utf-8")

    assert "lexical.models.lexical_source" not in domain_text
    assert "domain.lexical.lexical_source" not in kernel_text


def test_architecture_decision_is_retain_both():
    """
    Explicit architecture decision.

    Domain and kernel LexicalSource models are intentionally
    retained as separate representations.

    Mapping may be introduced later only if a real boundary
    requires conversion between them.
    """

    assert DOMAIN_SOURCE != KERNEL_SOURCE
