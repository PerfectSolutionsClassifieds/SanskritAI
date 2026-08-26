
from __future__ import annotations

import pytest

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


class ConcreteResolutionContributor(
    ResolutionContributor,
):
    """
    Minimal concrete implementation used only to test
    the ResolutionContributor contract.

    The concrete implementation is intentionally stateless
    and therefore declares empty slots.
    """

    __slots__ = ()

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Return the supplied aggregate unchanged.

        The contributor contract requires the supplied
        context to represent the same immutable value as
        the aggregate context.

        Equality is intentionally used instead of identity
        because ResolutionContext is an immutable value object.
        """

        assert aggregate.context == context

        return aggregate


def make_context(
    subject: str = "देवोऽस्ति",
) -> ResolutionContext:
    """
    Create a deterministic ResolutionContext for testing.
    """

    return ResolutionContext(
        identifier="context-1",
        subject=subject,
    )


def make_result(
    context: ResolutionContext | None = None,
) -> ResolutionResult:
    """
    Create a deterministic ResolutionResult for testing.

    A context may be supplied explicitly when identity
    preservation needs to be tested.
    """

    if context is None:
        context = make_context()

    return ResolutionResult(
        context=context,
    )


def test_resolution_contributor_is_abstract():

    assert (
        "contribute"
        in ResolutionContributor.__abstractmethods__
    )


def test_resolution_contributor_cannot_be_instantiated():

    with pytest.raises(TypeError):
        ResolutionContributor()


def test_concrete_contributor_is_instance_of_contract():

    contributor = ConcreteResolutionContributor()

    assert isinstance(
        contributor,
        ResolutionContributor,
    )


def test_contributor_has_no_instance_dict():

    contributor = ConcreteResolutionContributor()

    assert not hasattr(
        contributor,
        "__dict__",
    )


def test_contributor_uses_empty_slots():

    assert ResolutionContributor.__slots__ == ()


def test_concrete_contributor_uses_empty_slots():

    assert (
        ConcreteResolutionContributor.__slots__
        == ()
    )


def test_contributor_has_no_own_dict_descriptor():

    assert (
        "__dict__"
        not in ResolutionContributor.__dict__
    )


def test_concrete_contributor_has_no_own_dict_descriptor():

    assert (
        "__dict__"
        not in ConcreteResolutionContributor.__dict__
    )


def test_default_display_name_is_class_name():

    contributor = ConcreteResolutionContributor()

    assert (
        contributor.display_name
        == "ConcreteResolutionContributor"
    )


def test_display_text_delegates_to_display_name():

    contributor = ConcreteResolutionContributor()

    assert (
        contributor.display_text
        == contributor.display_name
    )


def test_display_description_is_canonical():

    contributor = ConcreteResolutionContributor()

    assert (
        contributor.display_description
        == (
            "Contributes one linguistic resolution stage "
            "to the aggregate ResolutionResult."
        )
    )


def test_contributor_is_displayable():

    contributor = ConcreteResolutionContributor()

    assert contributor.is_displayable is True


def test_to_display_string_uses_display_text():

    contributor = ConcreteResolutionContributor()

    assert (
        contributor.to_display_string()
        == contributor.display_text
    )


def test_contribute_receives_aggregate_and_context():

    contributor = ConcreteResolutionContributor()

    context = make_context()

    aggregate = ResolutionResult(
        context=context,
    )

    result = contributor.contribute(
        aggregate=aggregate,
        context=context,
    )

    assert result is aggregate


def test_contributor_preserves_aggregate_context():

    contributor = ConcreteResolutionContributor()

    context = make_context()

    aggregate = ResolutionResult(
        context=context,
    )

    result = contributor.contribute(
        aggregate,
        context,
    )

    assert result.context is context


def test_contributor_accepts_equivalent_immutable_context():

    contributor = ConcreteResolutionContributor()

    aggregate_context = make_context()
    supplied_context = make_context()

    assert aggregate_context == supplied_context
    assert aggregate_context is not supplied_context

    aggregate = ResolutionResult(
        context=aggregate_context,
    )

    result = contributor.contribute(
        aggregate,
        supplied_context,
    )

    assert result is aggregate
    assert result.context is aggregate_context


def test_contributor_rejects_different_context():

    contributor = ConcreteResolutionContributor()

    aggregate_context = make_context(
        subject="देवोऽस्ति",
    )

    different_context = make_context(
        subject="रामः गच्छति",
    )

    aggregate = ResolutionResult(
        context=aggregate_context,
    )

    with pytest.raises(AssertionError):
        contributor.contribute(
            aggregate,
            different_context,
        )


def test_contributor_is_stateless():

    contributor = ConcreteResolutionContributor()

    first_context = make_context()
    second_context = make_context()

    assert first_context == second_context
    assert first_context is not second_context

    first = contributor.contribute(
        make_result(first_context),
        first_context,
    )

    second = contributor.contribute(
        make_result(second_context),
        second_context,
    )

    assert first == second


def test_contributor_does_not_mutate_aggregate():

    contributor = ConcreteResolutionContributor()

    context = make_context()
    aggregate = make_result(context)

    result = contributor.contribute(
        aggregate,
        context,
    )

    assert result is aggregate
    assert result.context is context
    assert result.context == context


def test_string_representation_uses_display_text():

    contributor = ConcreteResolutionContributor()

    assert str(contributor) == contributor.display_text
