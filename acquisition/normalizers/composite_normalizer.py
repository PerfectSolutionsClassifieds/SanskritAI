
from __future__ import annotations

"""
SanskritAI
==========

Composite Normalizer

Executes multiple normalizers sequentially as a normalization
pipeline.

Responsibilities
----------------
* Compose multiple normalizers
* Execute them in order
* Produce a single normalized result
* Provide pipeline management utilities

This class intentionally does NOT implement any normalization
logic itself. Each transformation is delegated to the contained
normalizers.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from collections.abc import Iterable, Iterator

from SanskritAI.acquisition.normalizers.base_normalizer import (
    BaseNormalizer,
)


class CompositeNormalizer(BaseNormalizer):
    """
    Executes multiple normalizers sequentially.

    Example
    -------

    pipeline = CompositeNormalizer([
        UnicodeNormalizer(),
        SanskritNormalizer(),
        LineEndingNormalizer(),
        WhitespaceNormalizer(),
    ])

    normalized = pipeline.normalize(text)
    """

    def __init__(
        self,
        normalizers: Iterable[BaseNormalizer] | None = None,
    ) -> None:
        super().__init__()

        self._normalizers: list[BaseNormalizer] = []

        if normalizers is not None:
            for normalizer in normalizers:
                self.add(normalizer)

    # ---------------------------------------------------------
    # BaseNormalizer API
    # ---------------------------------------------------------

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Applies every normalizer sequentially.
        """

        result = self.ensure_text(text)

        for normalizer in self._normalizers:
            result = normalizer.normalize(result)

        return result

    # ---------------------------------------------------------
    # Pipeline Management
    # ---------------------------------------------------------

    def add(
        self,
        normalizer: BaseNormalizer,
    ) -> "CompositeNormalizer":
        """
        Appends a normalizer to the pipeline.

        Returns
        -------
        CompositeNormalizer

        Enables fluent chaining.
        """

        if not isinstance(normalizer, BaseNormalizer):
            raise TypeError(
                "normalizer must be an instance of "
                "BaseNormalizer."
            )

        self._normalizers.append(normalizer)

        return self

    def extend(
        self,
        normalizers: Iterable[BaseNormalizer],
    ) -> "CompositeNormalizer":
        """
        Appends multiple normalizers.
        """

        for normalizer in normalizers:
            self.add(normalizer)

        return self

    def clear(self) -> None:
        """
        Removes every normalizer from the pipeline.
        """

        self._normalizers.clear()

    # ---------------------------------------------------------
    # Accessors
    # ---------------------------------------------------------

    @property
    def normalizers(self) -> tuple[BaseNormalizer, ...]:
        """
        Immutable view of the pipeline.
        """

        return tuple(self._normalizers)

    @property
    def count(self) -> int:
        """
        Number of normalizers.
        """

        return len(self._normalizers)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no normalizers are registered.
        """

        return not self._normalizers

    # ---------------------------------------------------------
    # Container Protocol
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self._normalizers)

    def __iter__(self) -> Iterator[BaseNormalizer]:
        return iter(self._normalizers)

    def __getitem__(
        self,
        index: int,
    ) -> BaseNormalizer:
        return self._normalizers[index]

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        names = ", ".join(
            normalizer.__class__.__name__
            for normalizer in self._normalizers
        )

        return (
            "CompositeNormalizer("
            f"count={len(self)}, "
            f"pipeline=[{names}])"
        )
