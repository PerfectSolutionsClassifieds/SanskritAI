from __future__ import annotations

"""
SanskritAI
==========

Paninian Sutra Registration

Canonical registration infrastructure for executable
Paninian Sūtras.

Purpose
-------

Provides the registration decorator used by every
implemented sūtra.

Example
-------

@register_paninian_sutra
class Sutra111VrddhirAdaic(...):
    ...

Registration occurs automatically at import time.

This module intentionally contains no discovery logic.
Discovery is handled by PaninianSutraLoader.

Version
-------
v1.0.0
"""

from collections.abc import Callable
from typing import TypeVar

from SanskritAI.domain.panini.paninian_rule import PaninianRule

# ---------------------------------------------------------
# Types
# ---------------------------------------------------------

RuleT = TypeVar(
    "RuleT",
    bound=type[PaninianRule],
)

# ---------------------------------------------------------
# Canonical registry storage
# ---------------------------------------------------------

_DEFAULT_REGISTRY_NAME = "panini"

# registry_name -> sutra_number -> rule class
_SUTRA_REGISTRIES: dict[
    str,
    dict[str, type[PaninianRule]],
] = {
    _DEFAULT_REGISTRY_NAME: {},
}


# ---------------------------------------------------------
# Registry access
# ---------------------------------------------------------

def get_registry(
    registry_name: str = _DEFAULT_REGISTRY_NAME,
) -> dict[str, type[PaninianRule]]:
    """
    Returns the requested registry.

    Creates it if necessary.
    """

    return _SUTRA_REGISTRIES.setdefault(
        registry_name,
        {},
    )


def registered_sutra_numbers(
    registry_name: str = _DEFAULT_REGISTRY_NAME,
) -> tuple[str, ...]:
    """
    Returns all registered sūtra numbers.
    """

    return tuple(
        sorted(
            get_registry(registry_name),
        )
    )


def clear_registry(
    registry_name: str = _DEFAULT_REGISTRY_NAME,
) -> None:
    """
    Clears one registry.

    Intended primarily for testing.
    """

    get_registry(registry_name).clear()


# ---------------------------------------------------------
# Registration
# ---------------------------------------------------------

def register_paninian_sutra(
    cls: RuleT | None = None,
    *,
    registry_name: str = _DEFAULT_REGISTRY_NAME,
) -> RuleT | Callable[[RuleT], RuleT]:
    """
    Registers an executable Paninian Sūtra.

    May be used as

        @register_paninian_sutra

    or

        @register_paninian_sutra(
            registry_name="panini"
        )
    """

    def _register(
        rule_cls: RuleT,
    ) -> RuleT:

        try:
            instance = rule_cls()

        except Exception as exc:
            raise RuntimeError(
                f"Unable to instantiate "
                f"{rule_cls.__name__} during "
                f"registration."
            ) from exc

        sutra_number = instance.sutra_number

        registry = get_registry(
            registry_name,
        )

        if sutra_number in registry:
            raise ValueError(
                f"Sūtra '{sutra_number}' "
                f"is already registered."
            )

        registry[sutra_number] = rule_cls

        return rule_cls

    if cls is None:
        return _register

    return _register(cls)


# ---------------------------------------------------------
# Lookup
# ---------------------------------------------------------

def is_registered(
    sutra_number: str,
    registry_name: str = _DEFAULT_REGISTRY_NAME,
) -> bool:
    """
    Returns True if the sūtra is registered.
    """

    return (
        sutra_number
        in get_registry(registry_name)
    )


def get_registered_class(
    sutra_number: str,
    registry_name: str = _DEFAULT_REGISTRY_NAME,
) -> type[PaninianRule] | None:
    """
    Returns the registered rule class,
    or None.
    """

    return get_registry(
        registry_name,
    ).get(
        sutra_number,
    )
