import os

from django.core.management import call_command
from django.test import TestCase

import tablib
from dateutil.relativedelta import relativedelta

from vrl.selectielijst.management.commands.load_data_from_excel import (
    check_choice,
    parse_duration,
    prepare_procestype,
    prepare_resultaat,
)
from vrl.selectielijst.models import ProcesType, Resultaat

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "testdata.xls")
TESTDATA_2020_FILENAME = os.path.join(os.path.dirname(__file__), "testdata_2020.xls")


class LoadDataFromExcelTest(TestCase):
    """Test my custom command."""

    maxDiff = None

    def setUp(self):
        self.dataset = tablib.import_set(open(TESTDATA_FILENAME, "rb").read())

        self.jaar = 2017
        self.raw = {
            "Procestypenummer": 1,
            "Procestypenaam": "Instellen en inrichten organisatie",
            "Procestypeomschrijving": "Instellen en inrichten organisatie",
            "Procestypetoelichting": "Dit procestype betreft het instellen van een nieuw organisatieonderdeel of een nieuw orgaan waar het orgaan in deelneemt. Dit procestype betreft eveneens het inrichten van het eigen orgaan. Dit kan kleinschalig plaatsvinden bijvoorbeeld het wijzigen van de uitvoering van een wettelijke taak of grootschalig wanneer er een organisatiewijziging wordt doorgevoerd.",
            "procesobject": "De vastgestelde organisatie inrichting",
            "Nr.": "1.1",
            "Generiek / specifiek": "Generiek",
            "Resultaat": "Ingericht",
            "Omschrijving": "",
            "Herkomst": "Risicoanalyse",
            "Waardering": "Vernietigen",
            "Procestermijn": "Nihil",
            "Bewaartermijn": "10 jaar",
            "Toelichting": "Invoering nieuwe werkwijze",
            "Algemeen bestuur en inrichting organisatie": "",
            "Bedrijfsvoering en personeel": "Bedrijfsvoering en personeel",
            "Publieke informatie en registratie": "",
            "Burgerzaken": "",
            "Veiligheid": "",
            "Verkeer en vervoer": "",
            "Economie": "",
            "Onderwijs": "",
            "Sport, cultuur en recreatie": "",
            "Sociaal domein": "",
            "Volksgezondheid en milieu": "",
            "VHROSV": "",
            "Heffen belastingen etc": "",
            "Alle taakgebieden": "",
        }

        self.specifiek = self.raw.copy()
        self.specifiek.update({"Nr.": "1.1.2", "Generiek / specifiek": "Specifiek"})

    def test_check_choice_fail(self):
        """
        test check_choice function: Input string doesn't contain choice label or value
        """
        self.assertRaises(Exception, check_choice, ("some data", {"nihil": "Nihil"}))

    def test_check_choice_success_label(self):
        """
        test check_choice function: Input string contains choice label
        """
        choice = check_choice(
            "De bestaans- of geldigheidsduur van het procesobject",
            {
                "bestaansduur_procesobject": "De bestaans- of geldigheidsduur van het procesobject."
            },
        )

        self.assertEqual(choice, "bestaansduur_procesobject")

    def test_check_choice_success_value(self):
        """
        test check_choice function: Input string contains choice value
        """
        choice = check_choice(
            "Bewaren", {"blijvend_bewaren": "Het zaakdossier moet bewaard blijven"}
        )

        self.assertEqual(choice, "blijvend_bewaren")

    def test_check_choice_empty(self):
        """
        test check_choice function: Input string is empty
        """
        self.assertEqual(check_choice("", {"nihil": "Nihil"}), "")

    def test_parse_duration_empty(self):
        """
        test parse_duration function: if string is empty return None
        """
        self.assertIsNone(parse_duration(""))

    def test_parse_duration_direct(self):
        """
        test parse_duration function: if zero time of storage
        """
        self.assertEqual(parse_duration("Direct"), relativedelta(days=0))
        self.assertEqual(
            parse_duration(
                "Na kennisgeving van Minister dat de grond tot weigering of intrekking is vervallen terstond vernietigen"
            ),
            relativedelta(days=0),
        )

    def test_parse_duration_integer_period(self):
        """
        test parse_duration function: if dur_string contains integer period
        """
        self.assertEqual(parse_duration("10 jaar"), relativedelta(years=10))

        self.assertEqual(parse_duration("4 weken"), relativedelta(weeks=4))

        self.assertEqual(parse_duration("6 maanden"), relativedelta(months=6))

    def test_parse_duration_float_period(self):
        """
        test parse_duration function: if dur_string contains float period, like x.5
        """
        self.assertEqual(parse_duration("1,5 jaar"), relativedelta(years=1, months=6))

    def test_prepare_procestype(self):
        """
        test prepare_procestype function
        """
        self.assertDictEqual(
            prepare_procestype(self.raw, self.jaar),
            {
                "nummer": 1,
                "naam": "Instellen en inrichten organisatie",
                "jaar": self.jaar,
                "omschrijving": "Instellen en inrichten organisatie",
                "toelichting": "Dit procestype betreft het instellen van een nieuw organisatieonderdeel of een nieuw orgaan waar het orgaan in deelneemt. Dit procestype betreft eveneens het inrichten van het eigen orgaan. Dit kan kleinschalig plaatsvinden bijvoorbeeld het wijzigen van de uitvoering van een wettelijke taak of grootschalig wanneer er een organisatiewijziging wordt doorgevoerd.",
                "procesobject": "De vastgestelde organisatie inrichting",
            },
        )

    def test_prepare_resultaat_generiek(self):
        """
        test prepare_procestype function: all general cols + cols for generiek resultaat
        """
        proces_type = ProcesType.objects.create(
            **prepare_procestype(self.raw, self.jaar)
        )

        self.assertDictEqual(
            prepare_resultaat(self.raw),
            {
                "proces_type": proces_type,
                "generiek_resultaat": None,
                "nummer": 1,
                "naam": "Ingericht",
                "omschrijving": "",
                "herkomst": "Risicoanalyse",
                "waardering": "vernietigen",
                "procestermijn": "nihil",
                "bewaartermijn": relativedelta(years=10),
                "toelichting": "Invoering nieuwe werkwijze",
                "algemeen_bestuur_en_inrichting_organisatie": False,
                "bedrijfsvoering_en_personeel": True,
                "publieke_informatie_en_registratie": False,
                "burgerzaken": False,
                "veiligheid": False,
                "verkeer_en_vervoer": False,
                "economie": False,
                "onderwijs": False,
                "sport_cultuur_en_recreatie": False,
                "sociaal_domein": False,
                "volksgezonheid_en_milieu": False,
                "vhrosv": False,
                "heffen_belastingen": False,
                "alle_taakgebieden": False,
                "procestermijn_opmerking": "",
            },
        )

    def test_prepare_resultaat_specifiek(self):
        """
        test prepare_procestype function: cols for specifiek resultaat
        """
        proces_type = ProcesType.objects.create(
            **prepare_procestype(self.raw, self.jaar)
        )
        generiek_resultaat = Resultaat.objects.create(**prepare_resultaat(self.raw))

        specifiek = prepare_resultaat(self.specifiek)

        self.assertEqual(specifiek["generiek_resultaat"], generiek_resultaat)
        self.assertEqual(specifiek["nummer"], 2)

    def test_command_no_argument(self):
        """
        test command: fails if no arguments are provided
        """
        self.assertRaises(Exception, call_command)

    def test_command_save_procestype(self):
        """
        test handle method: test if could be created model object after prepare_procestype function
        """
        procestype_data = prepare_procestype(self.raw, self.jaar)

        proces_type = ProcesType.objects.create(**procestype_data)

        self.assertIsNotNone(proces_type.pk)

    def test_command_save_resultaat_generiek(self):
        """
        test handle method: if could be created model object after prepare_resultaat function
        """
        proces_type = ProcesType.objects.create(
            **prepare_procestype(self.raw, self.jaar)
        )
        generiek_resultaat_data = prepare_resultaat(self.raw)

        generiek_resultaat = Resultaat.objects.create(**generiek_resultaat_data)

        self.assertIsNotNone(generiek_resultaat.pk)
        self.assertTrue(generiek_resultaat.generiek)

    def test_command_resultaat_specifiek(self):
        """
        test handle method: test if could be created model object after prepare_resultaat function for specifiek case
        """
        proces_type = ProcesType.objects.create(
            **prepare_procestype(self.raw, self.jaar)
        )
        generiek_resultaat = Resultaat.objects.create(**prepare_resultaat(self.raw))
        specifiek_resultaat_data = prepare_resultaat(self.specifiek)

        specifiek_resultaat = Resultaat.objects.create(**specifiek_resultaat_data)

        self.assertIsNotNone(specifiek_resultaat.pk)
        self.assertTrue(specifiek_resultaat.specifiek)
        self.assertEqual(specifiek_resultaat.generiek_resultaat, generiek_resultaat)

    def test_command_success(self):
        """
        test handle method: read test data and write them into model. Check number of obs
        """
        call_command("load_data_from_excel", TESTDATA_FILENAME, self.jaar)

        # for Resultaat
        self.assertEqual(len(Resultaat.objects.all()), 305)
        # for ProcesType - count distinct nummer
        self.assertEqual(len(ProcesType.objects.all()), 29)

    def test_command_success_testdata_2020(self):
        """
        test handle method: read test data and write them into model. Check number of obs
        """
        call_command("load_data_from_excel", TESTDATA_2020_FILENAME, self.jaar)

        # for Resultaat
        self.assertEqual(len(Resultaat.objects.all()), 346)
        # for ProcesType - count distinct nummer
        self.assertEqual(len(ProcesType.objects.all()), 29)

    def test_command_not_unique_procestype(self):
        """
        test handle method: if Procestype objects with same nummer exists - update this object
        """
        unique_data = self.raw.copy()
        unique_data["Procestypenaam"] = "Unique procestype"
        # save object with nummer, which exists in xls file
        proces_type = ProcesType.objects.create(
            **prepare_procestype(unique_data, self.jaar)
        )

        call_command("load_data_from_excel", TESTDATA_FILENAME, self.jaar)

        # check that our command overwrote current object
        self.assertEqual(
            ProcesType.objects.get(nummer=proces_type.nummer).naam,
            "Instellen en inrichten organisatie",
        )

    def test_command_not_unique_resultaat(self):
        """
        test handle method:
        if Resultaat objects with same (nummer, processtype_id, generiek_resultaat_id)
        exists - update this object
        """
        unique_data = self.raw.copy()
        unique_data["Resultaat"] = "Unique resultaat"
        proces_type = ProcesType.objects.create(
            **prepare_procestype(unique_data, self.jaar)
        )
        resultaat = Resultaat.objects.create(**prepare_resultaat(unique_data))

        call_command("load_data_from_excel", TESTDATA_FILENAME, self.jaar)

        # check that our command overwrote current object
        self.assertEqual(
            Resultaat.objects.get(
                proces_type__id=proces_type.id,
                nummer=proces_type.nummer,
                generiek_resultaat__isnull=True,
            ).naam,
            "Ingericht",
        )
