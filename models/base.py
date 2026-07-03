"""
SanskritAI
Base Domain Model

Every domain object in SanskritAI inherits from BaseModel.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from uuid import uuid4
from typing import Any

from models.enums.status import Status


@dataclass
class BaseModel:
    """
    Base class for every SanskritAI object.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    persistent_id: str = ""

    version: str = "0.2.1"

    status: Status = Status.CREATED

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------

    def touch(self) -> None:
        """
        Update modification timestamp.
        """
        self.updated_at = datetime.utcnow()

    # --------------------------------------------------

    def set_status(self, status: Status) -> None:
        """
        Change processing status.
        """
        self.status = status
        self.touch()

    # --------------------------------------------------

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Store arbitrary metadata.
        """
        self.metadata[key] = value
        self.touch()

    # --------------------------------------------------

    def to_dict(self) -> dict:
        """
        Convert object into dictionary.
        """
        return asdict(self)

    # --------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict):
        """
        Construct object from dictionary.
        """
        return cls(**data)

    # --------------------------------------------------

    def summary(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, status={self.status.value})"
        )

    # --------------------------------------------------

    def __repr__(self) -> str:
        return self.summary()
