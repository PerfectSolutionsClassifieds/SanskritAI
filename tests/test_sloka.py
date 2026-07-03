from models.sloka import Sloka


def test_sloka_holds_text():
    sloka = Sloka(text="धर्म कर्म।")
    assert sloka.text == "धर्म कर्म।"
