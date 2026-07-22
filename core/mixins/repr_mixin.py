from __future__ import annotations

"""
SanskritAI
==========

Repr Mixin

Provides a consistent ``__repr__`` implementation for
framework objects.

The representation automatically includes all public
instance attributes.

Version
-------
v0.3.0
"""


class ReprMixin:
    """
    Reusable __repr__ implementation.
    """

    def __repr__(
        self,
    ) -> str:

        if hasattr(self, "__dict__"):

            fields = ", ".join(

                f"{name}={value!r}"

                for name, value in self.__dict__.items()

                if not name.startswith("_")

            )

        else:

            fields = ""

        return (

            f"{self.__class__.__name__}"

            f"({fields})"

        )
