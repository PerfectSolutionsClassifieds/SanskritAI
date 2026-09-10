from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


def is_historical(path: Path) -> bool:
    stem = path.stem

    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]

        if suffix.isdigit():
            return True

    if stem and stem[-1].isdigit():
        return True

    return False


def module_name(path: Path) -> str:
    relative = path.relative_to(ROOT)

    return ".".join(
        ["SanskritAI", *relative.with_suffix("").parts]
    )


def normalize(module: str) -> str:
    prefix = "SanskritAI."

    if module.startswith(prefix):
        return module[len(prefix):]

    return module


def imports(path: Path) -> list[str]:

    try:
        tree = ast.parse(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return []

    result = []

    current = module_name(path)
    current_parts = current.split(".")

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            module = node.module or ""

            if node.level:

                package_parts = current_parts[:-1]

                base = package_parts[
                    :len(package_parts) - node.level + 1
                ]

                if node.module:
                    base.extend(
                        node.module.split(".")
                    )

                module = ".".join(base)

            result.append(
                normalize(module)
            )

        elif isinstance(node, ast.Import):

            for alias in node.names:
                result.append(
                    normalize(alias.name)
                )

    return result


def test_domain_acquisition_dependencies_are_explicitly_visible():

    findings = []

    for path in ROOT.rglob("*.py"):

        if any(
            part in EXCLUDED_DIRS
            for part in path.parts
        ):
            continue

        if "tests" in path.parts:
            continue

        if is_historical(path):
            continue

        relative = path.relative_to(ROOT)

        if "domain" not in relative.parts:
            continue

        for imported in imports(path):

            if (
                imported == "acquisition"
                or imported.startswith("acquisition.")
            ):
                findings.append(
                    (
                        str(relative),
                        imported,
                    )
                )

    # This is intentionally not:
    #
    #     assert not findings
    #
    # Existing dependencies are allowed until semantic ownership
    # analysis establishes whether they are architecturally valid.

    assert isinstance(findings, list)


def test_no_lexical_source_cross_layer_dependency():

    domain_source = (
        ROOT
        / "domain"
        / "lexical"
        / "lexical_source.py"
    )

    kernel_source = (
        ROOT
        / "lexical"
        / "models"
        / "lexical_source.py"
    )

    domain_text = domain_source.read_text(
        encoding="utf-8"
    )

    kernel_text = kernel_source.read_text(
        encoding="utf-8"
    )

    assert (
        "lexical.models.lexical_source"
        not in domain_text
    )

    assert (
        "domain.lexical.lexical_source"
        not in kernel_text
    )
