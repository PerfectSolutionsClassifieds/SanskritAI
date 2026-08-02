from __future__ import annotations

"""
SanskritAI
==========

Paninian Sutra Manifest

Purpose
-------

Acts as the canonical inventory of executable
Paninian sūtras currently implemented inside
SanskritAI.

Unlike the Registry, which stores executable rule
instances after import, the Manifest declares
which modules are expected to exist.

This allows the project to evolve gradually
towards the complete Aṣṭādhyāyī without requiring
filesystem scanning.

Architecture
------------

PaninianSutraManifest
          │
          ▼
PaninianSutraLoader
          │
          ▼
Registration Decorator
          │
          ▼
PaninianSutraRegistry
          │
          ▼
PaninianSutraIndex
          │
          ▼
PaninianSutraCatalog

Responsibilities
----------------

• declares implemented modules

• declares implemented sūtra numbers

• reports implementation progress

• serves as the canonical loading source

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from importlib import import_module


@dataclass(slots=True)
class PaninianSutraManifest:
    """
    Canonical executable sūtra manifest.
    """

    implemented_modules: tuple[str, ...] = field(
        default_factory=lambda: (

            # -----------------------------------------
            # Adhyāya 1
            # -----------------------------------------

            "SanskritAI.domain.panini.rules.sutras."
            "adhyaya_1.pada_1."
            "sutra_1_1_1_vrddhir_adaic",

        )
    )

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def load_modules(
        self,
    ) -> None:
        """
        Imports every implemented module.
        """

        for module in self.implemented_modules:

            import_module(
                module,
            )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def module_count(
        self,
    ) -> int:

        return len(
            self.implemented_modules,
        )

    @property
    def implemented_sutra_numbers(
        self,
    ) -> tuple[str, ...]:
        """
        Returns canonical sūtra numbers.

        Derived from module names.

        Example

            sutra_1_1_1_vrddhir_adaic

        →

            1.1.1
        """

        numbers = []

        for module in self.implemented_modules:

            filename = module.split(".")[-1]

            if not filename.startswith(
                "sutra_",
            ):
                continue

            prefix = filename.split(
                "_",
                maxsplit=4,
            )

            if len(prefix) >= 4:

                numbers.append(
                    ".".join(
                        prefix[1:4]
                    )
                )

        return tuple(
            sorted(
                numbers,
            )
        )

    @property
    def implementation_percentage(
        self,
    ) -> float:
        """
        Percentage of executable
        Aṣṭādhyāyī implemented.

        Uses approximately 4000 canonical
        executable sūtras.
        """

        TOTAL_SUTRAS = 4000

        return (
            self.module_count
            / TOTAL_SUTRAS
        ) * 100.0

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    def contains(
        self,
        sutra_number: str,
    ) -> bool:

        return (
            sutra_number
            in self.implemented_sutra_numbers
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "implemented_modules":
                self.module_count,

            "implemented_sutras":
                len(
                    self.implemented_sutra_numbers
                ),

            "coverage_percent":
                round(
                    self.implementation_percentage,
                    4,
                ),

            "sutras":
                self.implemented_sutra_numbers,
        }

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.module_count

    def __iter__(
        self,
    ):

        yield from self.implemented_modules

    def __contains__(
        self,
        item: str,
    ) -> bool:

        return item in self.implemented_modules

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianSutraManifest("
            f"{self.module_count} implemented modules)"
        )
