from __future__ import annotations

"""
13R-8F-8 — LocalFileImporter canonical source-path repair

Canonical source:
    manifest.source.local_path

Compatibility fallback:
    manifest.metadata["source_path"]

Ownership:
    LocalFileImporter

No AcquisitionManifest schema change.
No Amarakośa-specific downloader.
"""

from pathlib import Path
import shutil


REPO_ROOT = Path("/content/SanskritAI").resolve()

TARGET = (
    REPO_ROOT
    / "acquisition"
    / "downloaders"
    / "local_file_importer.py"
)

BACKUP = TARGET.with_suffix(
    ".py.bak_13r8f8"
)


def main() -> None:
    print("=" * 72)
    print("13R-8F-8 — LocalFileImporter canonical path repair")
    print("=" * 72)

    if not TARGET.exists():
        raise FileNotFoundError(TARGET)

    original = TARGET.read_text(
        encoding="utf-8"
    )

    if "def _resolve_source_path(" in original:
        print(
            "Repair already present; no modification required."
        )
        return

    if BACKUP.exists():
        print(
            f"Backup already exists: {BACKUP}"
        )
    else:
        shutil.copy2(
            TARGET,
            BACKUP,
        )
        print(
            f"Backup created: {BACKUP}"
        )

    old_supports = '''    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if the manifest specifies a local source path.
        """
        source_path = manifest.get_metadata("source_path")
        return source_path is not None
'''

    new_supports = '''    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if the manifest specifies a local source path.

        Canonical source:
            manifest.source.local_path

        Compatibility fallback:
            manifest.metadata["source_path"]
        """
        return self._resolve_source_path(manifest) is not None
'''

    if old_supports not in original:
        raise RuntimeError(
            "Expected supports() block was not found. "
            "Abort without modifying production."
        )

    updated = original.replace(
        old_supports,
        new_supports,
        1,
    )

    old_download_start = '''        result = AcquisitionResult(source=manifest.source)
        source = manifest.get_metadata("source_path")
        if source is None:
            result.add_error(
                "Manifest metadata does not contain 'source_path'."
            )
            return self.finalize_result(result)
        source_path = Path(source)
'''

    new_download_start = '''        result = AcquisitionResult(source=manifest.source)
        source_path = self._resolve_source_path(manifest)

        if source_path is None:
            result.add_error(
                "Manifest does not contain a local source path."
            )
            return self.finalize_result(result)

        source_path = Path(source_path)
'''

    if old_download_start not in updated:
        raise RuntimeError(
            "Expected download() source-resolution block was not found. "
            "Abort without modifying production."
        )

    updated = updated.replace(
        old_download_start,
        new_download_start,
        1,
    )

    marker = '''    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
'''

    helper = '''    def _resolve_source_path(
        self,
        manifest: AcquisitionManifest,
    ) -> Path | None:
        """
        Resolve the canonical local source path.

        Precedence
        ----------
        1. CorpusSource.local_path
        2. metadata["source_path"] compatibility fallback
        3. None

        LocalFileImporter owns this normalization because it is the
        component that understands local filesystem acquisition.
        """
        source = manifest.source

        local_path = getattr(
            source,
            "local_path",
            None,
        )

        if local_path is not None:
            return Path(local_path)

        metadata_path = manifest.get_metadata(
            "source_path"
        )

        if metadata_path is not None:
            return Path(metadata_path)

        return None

'''

    if marker not in updated:
        raise RuntimeError(
            "Internal helper marker not found. "
            "Abort without modifying production."
        )

    updated = updated.replace(
        marker,
        marker + helper,
        1,
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
    )

    print()
    print(
        "Production file updated:",
        TARGET,
    )
    print(
        "Canonical resolution owner: LocalFileImporter"
    )
    print(
        "Canonical path: manifest.source.local_path"
    )
    print(
        "Compatibility fallback: metadata['source_path']"
    )
    print(
        "AcquisitionManifest schema changed: NO"
    )
    print(
        "Amarakośa-specific abstraction created: NO"
    )

    # ---------------------------------------------------------------
    # Syntax validation
    # ---------------------------------------------------------------

    import ast

    ast.parse(
        TARGET.read_text(
            encoding="utf-8"
        ),
        filename=str(TARGET),
    )

    print(
        "Written-file Python syntax: PASS"
    )

    print()
    print(
        "13R-8F-8 COMPLETE"
    )


if __name__ == "__main__":
    main()
