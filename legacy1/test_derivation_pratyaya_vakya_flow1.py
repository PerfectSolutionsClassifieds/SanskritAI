from __future__ import annotations

"""
End-to-end integration test for Dhatu + Pratyaya + Derivation
+ Vakya flow.

This file exercises the kernel flow:
- Dhatu lookup
- Pratyaya lookup
- Derivation
- Sandhi
- Samasa
- Vakya
"""

import unittest

import SanskritAI

from SanskritAI.domain.dhatu.default_dhatu_resolver import (
    DefaultDhatuResolver,
)
from SanskritAI.domain.dhatu.dhatu_factory import DhatuFactory
from SanskritAI.domain.derivation.default_derivation_resolver import (
    DefaultDerivationResolver,
)
from SanskritAI.domain.derivation.derivation_context import DerivationContext
from SanskritAI.domain.derivation.derivation_output_collection import (
    DerivationOutputCollection,
)
from SanskritAI.domain.pratyaya.default_pratyaya_resolver import (
    DefaultPratyayaResolver,
)
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_factory import PratyayaFactory
from SanskritAI.domain.sandhi.default_sandhi_resolver import (
    DefaultSandhiResolver,
)
from SanskritAI.domain.sandhi.sandhi_context import SandhiContext
from SanskritAI.domain.samasa.default_samasa_resolver import (
    DefaultSamasaResolver,
)
from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.vakya.default_vakya_resolver import (
    DefaultVakyaResolver,
)
from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_structure import VakyaStructure


class TestKernelFlow(unittest.TestCase):
    def test_end_to_end_flow(self) -> None:
        dhatu_collection = DhatuFactory.create_default_collection()
        pratyaya_collection = PratyayaFactory.create_default_collection()

        dhatu = dhatu_collection.get_by_root("भू")
        pratyaya = pratyaya_collection.get_by_identifier("pratyaya.kta")

        self.assertIsNotNone(dhatu)
        self.assertIsNotNone(pratyaya)

        derivation_result = DefaultDerivationResolver().analyze(
            DerivationContext(
                identifier="derivation-1",
                dhatu=dhatu,
                pratyaya=pratyaya,
            )
        )
        self.assertTrue(derivation_result.resolved)
        self.assertTrue(derivation_result.has_outputs)
        self.assertGreaterEqual(derivation_result.output_count, 1)
        self.assertIsNotNone(derivation_result.best_output)
        self.assertEqual(derivation_result.best_output.surface_form, "भूत")

        # Compatibility aliases during transition.
        self.assertTrue(derivation_result.has_analyses)
        self.assertEqual(
            derivation_result.analysis_count,
            derivation_result.output_count,
        )
        self.assertIsNotNone(derivation_result.best_analysis)
        self.assertEqual(
            derivation_result.best_analysis.surface_form,
            derivation_result.best_output.surface_form,
        )
        self.assertIsInstance(derivation_result.result, DerivationOutputCollection)
        self.assertEqual(
            derivation_result.result.count,
            derivation_result.output_count,
        )

        pratyaya_result = DefaultPratyayaResolver().analyze(
            PratyayaContext(
                identifier="pratyaya-1",
                subject="क्त",
            )
        )
        self.assertTrue(pratyaya_result.resolved)
        self.assertGreaterEqual(pratyaya_result.analysis_count, 1)
        self.assertIsNotNone(pratyaya_result.best_analysis)

        sandhi_result = DefaultSandhiResolver().resolve(
            SandhiContext(
                identifier="sandhi-1",
                subject="अ अ",
            )
        )
        self.assertTrue(sandhi_result.resolved)
        self.assertGreaterEqual(sandhi_result.candidate_count, 1)

        samasa_result = DefaultSamasaResolver().analyze(
            SamasaContext(
                identifier="samasa-1",
                subject="राज पुरुष",
                metadata={"samasa_hint": "tatpurusha"},
            )
        )
        self.assertTrue(samasa_result.resolved)
        self.assertGreaterEqual(samasa_result.analysis_count, 1)

        vakya_result = DefaultVakyaResolver().analyze(
            VakyaContext(
                identifier="vakya-1",
                subject="  भूतः ।  ",
                metadata={
                    "derivation": derivation_result,
                    "samasa": samasa_result,
                    "sandhi": sandhi_result,
                    "grammar": {"role": "कर्ता"},
                },
            )
        )
        self.assertTrue(vakya_result.resolved)
        self.assertGreaterEqual(vakya_result.analysis_count, 1)
        self.assertIsNotNone(vakya_result.best_analysis)

        # Compatibility / normalization path checks.
        self.assertIsInstance(
            vakya_result.context.metadata.get("vakya_structure"),
            VakyaStructure,
        )
        structure = vakya_result.context.metadata["vakya_structure"]
        self.assertEqual(structure.normalized_sentence, "भूतः")
        self.assertEqual(vakya_result.context.subject, "भूतः")
        self.assertIn("vakya_parse_result", vakya_result.context.metadata)
        self.assertIn("sentence_components", vakya_result.context.metadata)
        self.assertIn("vakya_roles", vakya_result.context.metadata)

        parse_result = vakya_result.context.metadata["vakya_parse_result"]
        self.assertGreaterEqual(parse_result.role_count, 1)
        self.assertTrue(parse_result.has_roles)

    def test_dhatu_lookup_still_works(self) -> None:
        dhatu_result = DefaultDhatuResolver().analyze(
            SanskritAI.domain.dhatu.dhatu_context.DhatuContext(
                identifier="dhatu-1",
                subject="भू",
            )
        )
        self.assertTrue(dhatu_result.resolved)


if __name__ == "__main__":
    unittest.main()
