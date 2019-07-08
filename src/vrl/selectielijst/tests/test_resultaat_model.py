from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import ProcesTypeFactory, ResultaatFactory


class ResultaatTests(TestCase):
    def test_generiek_omschrijving_forbidden(self):
        resultaat = ResultaatFactory.build(generiek_resultaat=None, omschrijving="foo")

        with self.assertRaises(ValidationError) as exc_context:
            resultaat.full_clean()

        self.assertIn("omschrijving", exc_context.exception.error_dict)

    def test_generiek_omschrijving_empty(self):
        resultaat = ResultaatFactory.build(generiek_resultaat=None, omschrijving="")

        # exc because proces_type has no PK yet (fast tests)
        with self.assertRaises(ValidationError) as exc_context:
            resultaat.full_clean()

        self.assertNotIn("omschrijving", exc_context.exception.error_dict)

    def test_specifiek_omschrijving_missing(self):
        generiek_resultaat = ResultaatFactory.create()

        resultaat = ResultaatFactory.build(
            generiek_resultaat=generiek_resultaat, omschrijving=""
        )

        with self.assertRaises(ValidationError) as exc_context:
            resultaat.full_clean()

        self.assertIn("omschrijving", exc_context.exception.error_dict)

    def test_specifiek_omschrijving_ok(self):
        generiek_resultaat = ResultaatFactory.create()

        resultaat = ResultaatFactory.build(
            generiek_resultaat=generiek_resultaat, omschrijving="foo"
        )

        with self.assertRaises(ValidationError) as exc_context:
            resultaat.full_clean()

        self.assertNotIn("omschrijving", exc_context.exception.error_dict)

    def test_generiek_specifiek_different_procestype(self):
        pt1, pt2 = ProcesTypeFactory.create_batch(2)

        generiek_resultaat = ResultaatFactory.create(proces_type=pt1)

        resultaat = ResultaatFactory.build(
            proces_type=pt2, generiek_resultaat=generiek_resultaat, omschrijving="foo"
        )

        with self.assertRaises(ValidationError) as exc_context:
            resultaat.full_clean()

        self.assertIn("proces_type", exc_context.exception.error_dict)

    def test_generiek_specifiek_same_procestype(self):
        generiek_resultaat = ResultaatFactory.create()

        resultaat = ResultaatFactory.build(
            proces_type=generiek_resultaat.proces_type,
            generiek_resultaat=generiek_resultaat,
            omschrijving="foo",
        )

        try:
            resultaat.full_clean()
        except ValidationError as exc:
            self.fail("Didn't pass validation", exc.error_dict)

    def test_generiek_resultaat(self):
        resultaat = ResultaatFactory.build(generiek_resultaat=None)

        self.assertTrue(resultaat.generiek)
        self.assertFalse(resultaat.specifiek)

    def test_specifiek_resultaat(self):
        parent = ResultaatFactory.create()

        resultaat = ResultaatFactory.build(generiek_resultaat=parent)

        self.assertFalse(resultaat.generiek)
        self.assertTrue(resultaat.specifiek)

    def test_volledig_nummer(self):
        generiek = ResultaatFactory.create(proces_type__nummer=4, nummer=2)
        specifiek = ResultaatFactory.create(
            proces_type=generiek.proces_type, generiek_resultaat=generiek, nummer=7
        )

        self.assertEqual(generiek.volledig_nummer, "4.2")
        self.assertEqual(specifiek.volledig_nummer, "4.2.7")
