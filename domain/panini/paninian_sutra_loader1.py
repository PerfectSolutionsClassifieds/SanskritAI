from __future__ import annotations

"""
SanskritAI
==========

Paninian Sūtra Loader

Discovers and imports executable Paninian Sūtras.

Purpose
-------

The loader performs automatic discovery of all
implemented Paninian sūtras.

Importing a module causes its

    @register_paninian_sutra

decorator to execute, automatically registering
the rule.

The loader itself never manipulates registries.

Architecture
------------

Filesystem

      ↓

Module Discovery

      ↓

Dynamic Import

      ↓

Registration Decorator

      ↓

PaninianSutraRegistry

Version
-------
v1.0.0
"""

from dataclasses import dataclass
import importlib
import pkgutil

import SanskritAI.domain.panini.rules.sutras as sutra_package


@dataclass(slots=True)
class PaninianSutraLoader:
    """
    Canonical Paninian Sūtra loader.
    """

    package = sutra_package

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover_modules(
        self,
    ) -> tuple[str, ...]:
        """
        Discovers every executable sutra module.
        """

        modules: list[str] = []

        prefix = self.package.__name__ + "."

        for module_info in pkgutil.walk_packages(
            self.package.__path__,
            prefix,
        ):

            if module_info.ispkg:
                continue

            module_name = module_info.name

            short_name = module_name.rsplit(
                ".",
                1,
            )[-1]

            if short_name.startswith(
                "sutra_",
            ):
                modules.append(
                    module_name,
                )

        return tuple(
            sorted(modules),
        )

    # ---------------------------------------------------------
    # Import
    # ---------------------------------------------------------

    def load_module(
        self,
        module_name: str,
    ) -> None:
        """
        Imports one module.
        """

        importlib.import_module(
            module_name,
        )

    def load_all(
        self,
    ) -> tuple[str, ...]:
        """
        Imports every discovered sūtra module.

        Registration occurs automatically through
        decorators.
        """

        loaded: list[str] = []

        for module in self.discover_modules():

            self.load_module(
                module,
            )

            loaded.append(
                module,
            )

        return tuple(
            loaded,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        modules = self.discover_modules()

        return {

            "package": self.package.__name__,

            "discovered_modules": len(modules),

            "modules": modules,

        }

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianSutraLoader("
            f"{self.package.__name__})"
        )
