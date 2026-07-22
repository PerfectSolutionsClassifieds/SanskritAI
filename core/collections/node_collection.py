from __future__ import annotations

"""
SanskritAI
==========

Node Collection

Reusable ordered collection for domain objects.

The collection preserves insertion order while providing a
lightweight abstraction over Python lists. It serves as the
foundation for managing child nodes throughout the framework.

Future versions may extend this class with:

- uniqueness constraints
- indexed lookup
- filtering
- sorting
- lazy evaluation
- event notifications

Version
-------
v0.3.0
"""

from collections.abc import Iterable, Iterator
from typing import Generic

from SanskritAI.core.typing import T


class NodeCollection(Generic[T]):
    """
    Ordered collection of domain objects.
    """

    def __init__(
        self,
        items: Iterable[T] | None = None,
    ) -> None:

        self._items: list[T] = list(items or [])

    # ---------------------------------------------------------
    # Modification
    # ---------------------------------------------------------

    def add(
        self,
        item: T,
    ) -> None:
        """
        Append an item.
        """

        self._items.append(item)

    # ---------------------------------------------------------

    def extend(
        self,
        items: Iterable[T],
    ) -> None:
        """
        Append multiple items.
        """

        self._items.extend(items)

    # ---------------------------------------------------------

    def remove(
        self,
        item: T,
    ) -> None:
        """
        Remove an item.
        """

        self._items.remove(item)

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove all items.
        """

        self._items.clear()

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def first(
        self,
    ) -> T | None:
        """
        Return the first item, if present.
        """

        return self._items[0] if self._items else None

    # ---------------------------------------------------------

    def last(
        self,
    ) -> T | None:
        """
        Return the last item, if present.
        """

        return self._items[-1] if self._items else None

    # ---------------------------------------------------------

    def to_list(
        self,
    ) -> list[T]:
        """
        Return a shallow copy of the collection.
        """

        return list(self._items)

    # ---------------------------------------------------------
    # Python Protocols
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[T]:

        return iter(self._items)

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> T:

        return self._items[index]

    # ---------------------------------------------------------

    def __contains__(
        self,
        item: T,
    ) -> bool:

        return item in self._items

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._items)

    # ---------------------------------------------------------

    def __bool__(
        self,
    ) -> bool:

        return bool(self._items)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(count={len(self)})"
        )
