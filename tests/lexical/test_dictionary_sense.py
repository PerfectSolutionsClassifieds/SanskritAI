"""
SanskritAI
==========

DictionarySense Unit Tests

Version:
    v0.3.0 Final
"""

from models.lexical import DictionarySense


def test() -> None:
    """
    Validate DictionarySense behavior.
    """

    sense = DictionarySense(
        sense_id="SENSE-0001",
        definition="Fire; the Vedic deity Agni.",
        language="en",
    )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    assert sense.sense_id == "SENSE-0001"

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    assert sense.definition == "Fire; the Vedic deity Agni."

    assert sense.language == "en"

    # ---------------------------------------------------------
    # Examples
    # ---------------------------------------------------------

    assert sense.example_count == 0

    sense.add_example("अग्निर्देवता।")

    sense.add_example("अग्निर्देवता。")  # Different punctuation; kept as a distinct example.

    sense.add_example("अग्निर्देवता।")  # Duplicate; ignored.

    assert sense.example_count == 2

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    data = sense.to_dict()

    assert data["sense_id"] == "SENSE-0001"
    assert data["definition"] == "Fire; the Vedic deity Agni."
    assert data["language"] == "en"
    assert len(data["examples"]) == 2

    print("DictionarySense test PASSED")


if __name__ == "__main__":
    test()
