from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.dhatu.default_dhatu_service import (
    DefaultDhatuService,
)
from SanskritAI.domain.dhatu.dhatu_context import (
    DhatuContext,
)
from SanskritAI.domain.dhatu.dhatu_resolver import (
    DhatuResolver,
)
from SanskritAI.domain.dhatu.dhatu_result import (
    DhatuResult,
)


class TestDefaultDhatuService:

    def test_creates_default_service(self):

        service = DefaultDhatuService()

        assert service is not None

    def test_default_resolver_is_created(self):

        service = DefaultDhatuService()

        assert isinstance(
            service.resolver,
            DhatuResolver,
        )

    def test_display_name(self):

        service = DefaultDhatuService()

        assert (
            service.display_name
            == "Default Dhatu Service"
        )

    def test_display_text(self):

        service = DefaultDhatuService()

        assert (
            service.display_text
            == "Default Dhatu Service"
        )

    def test_display_description(self):

        service = DefaultDhatuService()

        assert service.display_description

    def test_delegates_analysis_to_resolver(self):

        resolver = Mock(
            spec=DhatuResolver,
        )

        expected = Mock(
            spec=DhatuResult,
        )

        resolver.analyze.return_value = expected

        service = DefaultDhatuService(
            resolver=resolver,
        )

        context = DhatuContext(
            identifier="test",
            subject="भू",
        )

        result = service.analyze(
            context,
        )

        assert result is expected

        resolver.analyze.assert_called_once_with(
            context,
        )

    def test_resolve_is_alias_for_analyze(self):

        resolver = Mock(
            spec=DhatuResolver,
        )

        expected = Mock(
            spec=DhatuResult,
        )

        resolver.analyze.return_value = expected

        service = DefaultDhatuService(
            resolver=resolver,
        )

        context = DhatuContext(
            identifier="test",
            subject="भू",
        )

        result = service.resolve(
            context,
        )

        assert result is expected

        resolver.analyze.assert_called_once_with(
            context,
        )

    def test_service_is_immutable(self):

        service = DefaultDhatuService()

        try:
            service.resolver = Mock()
        except AttributeError:
            pass
        else:
            raise AssertionError(
                "DefaultDhatuService should be immutable."
            )

    def test_string_representation(self):

        service = DefaultDhatuService()

        assert str(service) == service.display_text
