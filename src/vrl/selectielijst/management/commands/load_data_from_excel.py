import re

from django.core.management.base import BaseCommand

import tablib
from dateutil.relativedelta import relativedelta
from vng_api_common.constants import Archiefnominatie

from vrl.selectielijst.constants import Procestermijnen
from vrl.selectielijst.models import ProcesType, Resultaat


def check_choice(string, choice_dict):
    if not string:
        return ""
    for k, v in choice_dict.items():
        if str(v)[:25] in string or string.lower() in k:
            return k
    raise Exception('"{}" is not found in choices'.format(string))


def parse_duration(dur_str):
    dur_str = str(dur_str)
    dur_str = dur_str.replace(",", ".").replace("  ", " ")

    if not dur_str:
        return

    if "Direct" in dur_str or "vernietigen" in dur_str:
        return relativedelta(days=0)

    NL_EN = {"jaar": "years", "weken": "weeks", "maanden": "months"}
    num, period = dur_str.split()
    period = NL_EN[period.lower()]
    num = float(num)
    if num.is_integer():
        rel_delta = relativedelta(**{period: num})
    else:  # non-integer periods are not supported
        quotient, remainder = divmod(num, 1)
        if remainder == 0.5 and period == "years":
            rel_delta = relativedelta(years=quotient, months=6)
        else:
            rel_delta = relativedelta(**{period: round(num)})
    return rel_delta


def prepare_procestype(raw, jaar):
    clean_data = {}
    clean_data["nummer"] = raw["Procestypenummer"]
    clean_data["naam"] = raw["Procestypenaam"]
    clean_data["omschrijving"] = raw["Procestypeomschrijving"]
    clean_data["toelichting"] = raw["Procestypetoelichting"]
    clean_data["procesobject"] = raw["procesobject"]
    clean_data["jaar"] = jaar
    return clean_data


def prepare_resultaat(raw):
    clean_data = {}

    proces_type = ProcesType.objects.get(nummer=raw["Procestypenummer"])
    clean_data["proces_type"] = proces_type

    if raw["Generiek / specifiek"] == "Specifiek":
        generiek_nummer = int(re.match(r"\d+\.(\d+)\.\d+", raw["Nr."]).group(1))
        clean_data["generiek_resultaat"] = Resultaat.objects.get(
            proces_type__id=proces_type.id,
            nummer=generiek_nummer,
            generiek_resultaat__isnull=True,
        )
    else:
        clean_data["generiek_resultaat"] = None

    clean_data["nummer"] = int(raw["Nr."].rsplit(".")[-1])
    clean_data["naam"] = raw["Resultaat"]
    clean_data["omschrijving"] = raw["Omschrijving"]
    clean_data["herkomst"] = raw["Herkomst"]

    if raw["Waardering"] == "Bewaren met uitzondering van zie toelichting":
        raw["Waardering"] = "Bewaren"
    clean_data["waardering"] = check_choice(raw["Waardering"], Archiefnominatie.labels)

    if "," in raw["Procestermijn"].replace("(", ","):
        opmerking, procestermijn = raw["Procestermijn"].replace("(", ",").split(",")
    else:
        opmerking, procestermijn = "", raw["Procestermijn"]
    clean_data["procestermijn"] = check_choice(procestermijn, Procestermijnen.labels)
    clean_data["procestermijn_opmerking"] = opmerking
    clean_data["bewaartermijn"] = parse_duration(raw["Bewaartermijn"])
    clean_data["toelichting"] = raw["Toelichting"]
    clean_data["algemeen_bestuur_en_inrichting_organisatie"] = bool(
        raw["Algemeen bestuur en inrichting organisatie"]
    )
    clean_data["bedrijfsvoering_en_personeel"] = bool(
        raw["Bedrijfsvoering en personeel"]
    )
    clean_data["publieke_informatie_en_registratie"] = bool(
        raw["Publieke informatie en registratie"]
    )
    clean_data["burgerzaken"] = bool(raw["Burgerzaken"])
    clean_data["veiligheid"] = bool(raw["Veiligheid"])
    clean_data["verkeer_en_vervoer"] = bool(raw["Verkeer en vervoer"])
    clean_data["economie"] = bool(raw["Economie"])
    clean_data["onderwijs"] = bool(raw["Onderwijs"])
    clean_data["sport_cultuur_en_recreatie"] = bool(raw["Sport, cultuur en recreatie"])
    clean_data["sociaal_domein"] = bool(raw["Sociaal domein"])
    clean_data["volksgezonheid_en_milieu"] = bool(raw["Volksgezondheid en milieu"])
    clean_data["vhrosv"] = bool(raw["VHROSV"])
    clean_data["heffen_belastingen"] = bool(raw["Heffen belastingen etc"])
    clean_data["alle_taakgebieden"] = bool(raw["Alle taakgebieden"])
    return clean_data


class Command(BaseCommand):
    help = "Load data from excel file to ProcesType and Resultaat"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to excel file")
        parser.add_argument("year", type=str, help="The year to which the data belongs")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        year = kwargs["year"]
        with open(file_path, "rb") as f:
            file_bin_input = f.read()
        dataset = tablib.import_set(file_bin_input)
        for raw in dataset.dict:
            # load to ProcesType
            processtype_data = prepare_procestype(raw, year)
            # if current nummer already exists - update it
            p, created = ProcesType.objects.update_or_create(
                nummer=processtype_data["nummer"],
                defaults=processtype_data,
                jaar=processtype_data["jaar"],
            )

            # load to Resultaat
            resultaat_data = prepare_resultaat(raw)
            # if current resultaat already exists - update it
            r, created = Resultaat.objects.update_or_create(
                proces_type=resultaat_data["proces_type"],
                generiek_resultaat=resultaat_data["generiek_resultaat"],
                nummer=resultaat_data["nummer"],
                defaults=resultaat_data,
            )
