
import unittest

from SanskritAI.acquisition.models.source_type import SourceType


class TestSourceType(unittest.TestCase):

    def test_from_string(self):
        self.assertEqual(
            SourceType.from_string("lexicon"),
            SourceType.LEXICON,
        )

    def test_unknown(self):
        self.assertEqual(
            SourceType.from_string("foobar"),
            SourceType.UNKNOWN,
        )

    def test_is_reference(self):
        self.assertTrue(SourceType.LEXICON.is_reference)
        self.assertTrue(SourceType.GRAMMAR.is_reference)
        self.assertFalse(SourceType.CORPUS.is_reference)

    def test_string(self):
        self.assertEqual(str(SourceType.CORPUS), "corpus")


if __name__ == "__main__":
    unittest.main()
