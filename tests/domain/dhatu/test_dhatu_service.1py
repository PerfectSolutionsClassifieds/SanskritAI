from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.dhatu.dhatu_context import (
    DhatuContext,
)

from SanskritAI.domain.dhatu.dhatu_resolver import (
    DhatuResolver,
)

from SanskritAI.domain.dhatu.dhatu_result import (
    DhatuResult,
)

from SanskritAI.domain.dhatu.dhatu_service import (
    DhatuService,
)


class TestDhatuService:

    def test_service_can_be_created(self):
        resolver = Mock(spec=DhatuResolver)

        service = DhatuService(
            resolver=resolver,
        )

        assert service is not None

    def test_display_name(self):
        resolver = Mock(spec=DhatuResolver)

        service = DhatuService(
            resolver=resolver,
        )

        assert service.display_name == "Dhatu Service"

    def test_display_text(self):
        resolver = Mock(spec=DhatuResolver)

        service = DhatuService(
            resolver=resolver,
        )

        assert service.display_text == "Dhatu Service"

    def test_display_description(self):
        resolver = Mock(spec=DhatuResolver)

        service = DhatuService(
            resolver=resolver,
        )

        assert (
            service.display_description
            == (
                "Application-facing façade for canonical "
                "Dhātu analysis."
            )
        )

    def test_analyze_delegates_to_resolver(self):
        resolver = Mock(spec=DhatuResolver)

        context = Mock(spec=DhatuContext)
        result = Mock(spec=DhatuResult)

        resolver.analyze.return_value = result

        service = DhatuService(
            resolver=resolver,
        )

        returned = service.analyze(
            context,
        )

        assert returned is result

        resolver.analyze.assert_called_once_with(
            context,
        )

    def test_resolve_is_alias_for_analyze(self):
        resolver = Mock(spec=DhatuResolver)

        context = Mock(spec=DhatuContext)
        result = Mock(spec=DhatuResult)

        resolver.analyze.return_value = result

        service = DhatuService(
            resolver=resolver,
        )

        returned = service.resolve(
            context,
        )

        assert returned is result

        resolver.analyze.assert_called_once_with(
            context,
        )

    def test_service_is_immutable(self):
        resolver = Mock(spec=DhatuResolver)

        service = DhatuService(
            resolver=resolver,
        )

        try:
            service.resolver = Mock()
        except AttributeError:
            pass
        else:
            raise AssertionError(
                "DhatuService should be immutable."
            )

    def test_string_representation(self):
        resolver = Mock(spec=DhatuResolver)

        service = DhatuService(
            resolver=resolver,
        )

        assert str(service) == "Dhatu Service"
