
from __future__ import annotations

"""
SanskritAI
==========

Paninian Sūtra Registration

Canonical registration infrastructure for executable
Paninian Sūtras.

The registration system supports the canonical decorator form:

    @register_paninian_sutra("1.1.1")
    class Sutra111VrddhirAdaic(...):
        ...

The explicit sūtra number supplied to the decorator is the
canonical registry key.

The rule class itself remains the executable object.

Architecture
------------

Paninian Sūtra Module
        │
        ▼
@register_paninian_sutra("1.1.1")
        │
        ▼
PaninianSutraRegistry
        │
        ▼
Rule Class
        │
        ▼
Rule Instance

Version
-------
v2.1.0
"""

from dataclasses import dataclass, field
from typing import Callable
from typing import TypeVar


from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)


RuleT = TypeVar(
    "RuleT",
    bound=type[PaninianRule],
)


# =========================================================
# Global Registry Store
# =========================================================

_REGISTRIES: dict[
    str,
    dict[str, type[PaninianRule]],
] = {}


# =========================================================
# Registry Access
# =========================================================

def get_registry(
    registry_name: str = "panini",
) -> dict[str, type[PaninianRule]]:
    """
    Returns the mutable registry dictionary for one
    registry namespace.

    The registry is created lazily.
    """

    return _REGISTRIES.setdefault(
        registry_name,
        {},
    )


def get_registered_class(
    sutra_number: str,
    registry_name: str = "panini",
) -> type[PaninianRule] | None:
    """
    Returns the registered rule class for one sūtra number.
    """

    registry = get_registry(
        registry_name,
    )

    return registry.get(
        sutra_number,
    )


def clear_registry(
    registry_name: str = "panini",
) -> None:
    """
    Clears one registry namespace.

    Primarily useful for isolated tests.
    """

    _REGISTRIES.pop(
        registry_name,
        None,
    )


# =========================================================
# Registration Decorator
# =========================================================

def register_paninian_sutra(
    sutra_number: str,
    registry_name: str = "panini",
) -> Callable[
    [RuleT],
    RuleT,
]:
    """
    Registers one executable Paninian Sūtra.

    Canonical usage
    ---------------

        @register_paninian_sutra("1.1.1")
        class Sutra111VrddhirAdaic(SamjnaRule):
            ...

    Parameters
    ----------
    sutra_number:
        Canonical Aṣṭādhyāyī sūtra number.

    registry_name:
        Registry namespace. Defaults to ``"panini"``.

    Returns
    -------
    decorator
        A class decorator which registers the supplied
        PaninianRule subclass.

    Notes
    -----
    Registration validates that the class can be instantiated
    and that its metadata is internally consistent with the
    supplied sūtra number.
    """

    if not isinstance(
        sutra_number,
        str,
    ):
        raise TypeError(
            "sutra_number must be a string."
        )

    sutra_number = sutra_number.strip()

    if not sutra_number:
        raise ValueError(
            "sutra_number cannot be empty."
        )

    if not registry_name:
        raise ValueError(
            "registry_name cannot be empty."
        )

    def decorator(
        rule_cls: RuleT,
    ) -> RuleT:
        """
        Register the decorated PaninianRule class.
        """

        if not isinstance(
            rule_cls,
            type,
        ):
            raise TypeError(
                "register_paninian_sutra must decorate "
                "a PaninianRule class."
            )

        if not issubclass(
            rule_cls,
            PaninianRule,
        ):
            raise TypeError(
                f"{rule_cls.__name__} must inherit "
                "from PaninianRule."
            )

        # -------------------------------------------------
        # Validate executable construction
        # -------------------------------------------------

        try:
            instance = rule_cls()

        except Exception as exc:
            raise RuntimeError(
                f"Unable to instantiate "
                f"{rule_cls.__name__} during "
                f"registration of sūtra "
                f"{sutra_number}."
            ) from exc

        # -------------------------------------------------
        # Validate metadata
        # -------------------------------------------------

        metadata = instance.metadata

        if metadata is None:
            raise ValueError(
                f"{rule_cls.__name__} returned no metadata."
            )

        # -------------------------------------------------
        # Validate canonical sūtra number
        # -------------------------------------------------

        metadata_sutra_number = getattr(
            instance,
            "sutra_number",
            None,
        )

        if (
            metadata_sutra_number
            and metadata_sutra_number != sutra_number
        ):
            raise ValueError(
                f"Sūtra number mismatch for "
                f"{rule_cls.__name__}: "
                f"decorator specifies "
                f"{sutra_number!r}, but rule metadata "
                f"specifies "
                f"{metadata_sutra_number!r}."
            )

        # -------------------------------------------------
        # Register
        # -------------------------------------------------

        registry = get_registry(
            registry_name,
        )

        existing = registry.get(
            sutra_number,
        )

        if (
            existing is not None
            and existing is not rule_cls
        ):
            raise ValueError(
                f"Paninian Sūtra "
                f"{sutra_number} is already registered "
                f"by {existing.__name__}."
            )

        registry[
            sutra_number
        ] = rule_cls

        return rule_cls

    return decorator


# =========================================================
# Registry Object
# =========================================================

@dataclass(slots=True)
class PaninianSutraRegistration:
    """
    Small diagnostic façade over a Paninian registry.
    """

    registry_name: str = "panini"

    @property
    def registry(
        self,
    ) -> dict[str, type[PaninianRule]]:
        return get_registry(
            self.registry_name,
        )

    @property
    def count(
        self,
    ) -> int:
        return len(
            self.registry,
        )

    @property
    def sutra_numbers(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            sorted(
                self.registry.keys(),
            )
        )

    def contains(
        self,
        sutra_number: str,
    ) -> bool:
        return sutra_number in self.registry

    def __len__(
        self,
    ) -> int:
        return self.count

    def __iter__(self):
        yield from self.sutra_numbers

    def __str__(
        self,
    ) -> str:
        return (
            "PaninianSutraRegistration("
            f"{self.registry_name}, "
            f"{self.count} sūtras)"
        )
