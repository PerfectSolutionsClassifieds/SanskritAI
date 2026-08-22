
from SanskritAI.acquisition.models.source_license import SourceLicense


def test_license_values():
    assert SourceLicense.PUBLIC_DOMAIN.value == "public_domain"
    assert SourceLicense.CC0.value == "cc0"
    assert SourceLicense.CC_BY.value == "cc_by"
    assert SourceLicense.PROPRIETARY.value == "proprietary"
    assert SourceLicense.UNKNOWN.value == "unknown"


def test_open_licenses():
    open_licenses = (
        SourceLicense.PUBLIC_DOMAIN,
        SourceLicense.CC0,
        SourceLicense.CC_BY,
        SourceLicense.CC_BY_SA,
        SourceLicense.OPEN_DATA,
        SourceLicense.MIT,
        SourceLicense.APACHE_2,
        SourceLicense.BSD,
    )

    for license_type in open_licenses:
        assert license_type.is_open


def test_non_open_licenses():
    for license_type in (
        SourceLicense.CC_BY_NC,
        SourceLicense.CC_BY_NC_SA,
        SourceLicense.GPL,
        SourceLicense.LGPL,
        SourceLicense.PROPRIETARY,
        SourceLicense.RESTRICTED,
        SourceLicense.RESEARCH,
        SourceLicense.UNKNOWN,
    ):
        assert not license_type.is_open


def test_attribution_requirements():
    for license_type in (
        SourceLicense.CC_BY,
        SourceLicense.CC_BY_SA,
        SourceLicense.CC_BY_NC,
        SourceLicense.CC_BY_NC_SA,
    ):
        assert license_type.requires_attribution

    assert not SourceLicense.PUBLIC_DOMAIN.requires_attribution
    assert not SourceLicense.CC0.requires_attribution


def test_commercial_use():
    commercial = (
        SourceLicense.PUBLIC_DOMAIN,
        SourceLicense.CC0,
        SourceLicense.CC_BY,
        SourceLicense.CC_BY_SA,
        SourceLicense.OPEN_DATA,
        SourceLicense.MIT,
        SourceLicense.APACHE_2,
        SourceLicense.BSD,
    )

    for license_type in commercial:
        assert license_type.allows_commercial_use

    assert not SourceLicense.CC_BY_NC.allows_commercial_use
    assert not SourceLicense.CC_BY_NC_SA.allows_commercial_use


def test_permission_required():
    for license_type in (
        SourceLicense.PROPRIETARY,
        SourceLicense.RESTRICTED,
        SourceLicense.RESEARCH,
        SourceLicense.UNKNOWN,
    ):
        assert license_type.requires_permission


def test_from_string():
    assert (
        SourceLicense.from_string("cc_by")
        is SourceLicense.CC_BY
    )

    assert (
        SourceLicense.from_string("CC_BY")
        is SourceLicense.CC_BY
    )

    assert (
        SourceLicense.from_string(" public_domain ")
        is SourceLicense.PUBLIC_DOMAIN
    )


def test_unknown_license():
    assert (
        SourceLicense.from_string("not-a-license")
        is SourceLicense.UNKNOWN
    )


def test_string_representation():
    assert str(SourceLicense.MIT) == "mit"
