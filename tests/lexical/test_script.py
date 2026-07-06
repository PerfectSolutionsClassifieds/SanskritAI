"""
SanskritAI
==========

Script Enumeration Tests

Version:
    v0.3.0 Final
"""

from models.enums.script import Script


def test() -> None:
    """
    Validate the Script enumeration.
    """

    # ---------------------------------------------------------
    # Basic enumeration
    # ---------------------------------------------------------

    assert len(Script) > 0

    assert Script.DEVANAGARI.value == "Devanagari"

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    print("=" * 60)
    print("Available Scripts")
    print("=" * 60)

    for script in Script:
        print(f"{script.name:<15} -> {script.value}")

    print()
    print("Script enumeration test PASSED")


if __name__ == "__main__":
    test()
