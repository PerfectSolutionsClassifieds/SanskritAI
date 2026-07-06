"""
SanskritAI
==========

Language Enumeration Tests

Version:
    v0.3.0 Final
"""

from models.enums.language import Language


def test() -> None:
    """
    Validate the Language enumeration.
    """

    # ---------------------------------------------------------
    # Basic enumeration
    # ---------------------------------------------------------

    assert len(Language) > 0

    assert Language.SANSKRIT.value == "Sanskrit"

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    print("=" * 60)
    print("Available Languages")
    print("=" * 60)

    for language in Language:
        print(f"{language.name:<15} -> {language.value}")

    print()
    print("Language enumeration test PASSED")


if __name__ == "__main__":
    test()
