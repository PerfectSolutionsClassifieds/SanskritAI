from __future__ import annotations

"""
SanskritAI
==========

Capability Provider

Defines a lightweight mixin for components that advertise a
CapabilityProfile.

Unlike CapabilityProfile, which is an immutable value object,
CapabilityProvider represents the runtime capability interface
implemented by components.

Typical providers include:

- Parser
- Morphological Analyzer
- Sandhi Engine
- Dictionary
- Corpus
- AI Backend
- Import Pipeline
- Plugin

Architecture
------------

CapabilityProvider
        │
        ▼
CapabilityProfile
        │
        ▼
CapabilitySet
        │
        ▼
Capability

Version
-------
v0.6.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.capabilities.capability import Capability
from SanskritAI.core.capabilities.capability_profile import CapabilityProfile


class CapabilityProvider(ABC):
    """
    Mixin for components that advertise capabilities.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def capability_profile(self) -> CapabilityProfile:
        """
        Returns the immutable capability profile of this
        component.
        """
        raise NotImplementedError

    @property
    def capabilities(self):
        """
        Convenience accessor for the advertised capabilities.
        """
        return self.capability_profile.capabilities

    def supports(
        self,
        capability: Capability,
    ) -> bool:
        """
        Determines whether this component advertises the supplied
        capability.
        """
        return self.capability_profile.supports(capability)
