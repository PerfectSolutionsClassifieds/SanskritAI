
"""
SanskritAI
==========

Module:
    domain.panini.paninian_sutra_loader

Description:
    Canonical executable Paninian Sūtra loader.

    Loads executable Paninian Sūtras declared by the
    canonical PaninianSutraManifest.

    The Manifest is the single source of truth.

Version:
    v2.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
import importlib

from SanskritAI.domain.panini.paninian_sutra_manifest import (
    PaninianSutraManifest,
)


@dataclass(slots=True)
class PaninianSutraLoader:
    """
    Canonical executable sūtra loader.
    """

    manifest: PaninianSutraManifest = field(
        default_factory=PaninianSutraManifest
    )

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover_modules(self) -> tuple[str, ...]:
        """
        Returns the canonical executable
        module list.

        The manifest owns this information.
        """

        return self.manifest.implemented_modules

    # ---------------------------------------------------------
    # Import
    # ---------------------------------------------------------

    def load_module(
        self,
        module_name: str,
    ) -> None:
        """
        Imports one executable sūtra module.
        """

        importlib.import_module(module_name)

    def load_all(self) -> tuple[str, ...]:
        """
        Imports every executable module declared
        by the manifest.
        """

        loaded: list[str] = []

        for module in self.discover_modules():
            self.load_module(module)
            loaded.append(module)

        return tuple(loaded)

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def module_count(self) -> int:
        return len(self.manifest)

    @property
    def implemented_sutras(self) -> tuple[str, ...]:
        return self.manifest.implemented_sutra_numbers

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> dict:
        """
        Returns loader summary.
        """

        return {
            "module_count": self.module_count,
            "implemented_sutras": self.implemented_sutras,
            "manifest": self.manifest.summary(),
        }

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.module_count

    def __iter__(self):
        yield from self.discover_modules()

    def __str__(self) -> str:
        return (
            "PaninianSutraLoader("
            f"{self.module_count} executable modules)"
        )
