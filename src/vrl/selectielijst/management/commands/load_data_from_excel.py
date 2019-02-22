import re
from dateutil.relativedelta import relativedelta
from xlrd import open_workbook

from django.core.management.base import BaseCommand

from vrl.selectielijst.models import ProcesType, Resultaat
from vrl.selectielijst.constants import ArchiefNominaties, Procestermijnen


# python src/manage.pload_data_from_excel /home/anna/Downloads/20170704-ontwerpselectielijst_opsomming_excel_definitief_versie2_0.xls
# curl -X POST http://127.0.0.1:8081/api/v1/resultaten -H "Content-Type: application/json" --data @/home/anna/Downloads/test_procestermijn_nihil.json

def read_xls_row_to_dict(sheet):
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

    for row_index in range(1, sheet.nrows):
        yield {keys[col_index]: sheet.cell(row_index, col_index).value
               for col_index in range(sheet.ncols)}


def check_choice(string, choice_dict):
    if not string:
        return ''
    for k, v in choice_dict.items():
        if str(v)[:25] in string:
            return k
    raise Exception('"{}" is not found in choices'.format(string))


def parse_duration(dur_str):
    dur_str = str(dur_str)
    dur_str = dur_str.replace(',', '.').replace('  ', ' ')

    if not dur_str:
        return

    if 'Direct' in dur_str or 'vernietigen' in dur_str:
        return relativedelta(days=0)

    NL_EN = {'jaar': 'years',
             'weken': 'weeks',
             'maanden': 'months'}
    num, period = dur_str.split()
    period = NL_EN[period.lower()]
    num = float(num)
    if num.is_integer():
        rel_delta = relativedelta(**{period: num})
    else:  # non-integer periods are not supported
        i, d = divmod(num, 1)
        if d == 0.5 and period == 'years':
            rel_delta = relativedelta(years=i, months=6)
        else:
            rel_delta = relativedelta(**{period: round(num)})
    return rel_delta


def prepare_procestype(raw):
    clean_data = {}
    clean_data['nummer'] = raw['Procestypenummer']
    clean_data['naam'] = raw['Procestypenaam']
    clean_data['omschrijving'] = raw['Procestypeomschrijving']
    clean_data['toelichting'] = raw['Procestypetoelichting']
    clean_data['procesobject'] = raw['procesobject']
    return clean_data


def prepare_resultaat(raw):
    clean_data = {}

    proces_type = ProcesType.objects.get(nummer=raw['Procestypenummer'])
    clean_data['proces_type'] = proces_type

    if raw['Generiek / specifiek'] == 'Specifiek':
        generiek_nummer = int(re.match(r"\d+\.(\d+)\.\d+", raw['Nr.']).group(1))
        clean_data['generiek_resultaat'] = Resultaat.objects.filter(proces_type__id=proces_type.id,
                                                                    nummer=generiek_nummer,
                                                                    generiek_resultaat__isnull=True)[0]
    else:
        clean_data['generiek_resultaat'] = None

    clean_data['nummer'] = int(re.match(r".*\.(\d+)", raw['Nr.']).group(1))
    clean_data['naam'] = raw['Resultaat']
    clean_data['omschrijving'] = raw['Omschrijving']
    clean_data['herkomst'] = raw['Herkomst']
    clean_data['waardering'] = check_choice(raw['Waardering'], ArchiefNominaties.labels)

    if ',' in raw['Procestermijn'].replace('(', ','):
        opmerking, procestermijn = raw['Procestermijn'].replace('(', ',').split(',')
    else:
        opmerking, procestermijn = None, raw['Procestermijn']
    clean_data['procestermijn'] = check_choice(procestermijn, Procestermijnen.labels)
    clean_data['procestermijn_opmerking'] = opmerking
    clean_data['bewaartermijn'] = parse_duration(raw['Bewaartermijn'])
    clean_data['toelichting'] = raw['Toelichting']
    clean_data['algemeen_bestuur_en_inrichting_organisatie'] = bool(raw['Algemeen bestuur en inrichting organisatie'])
    clean_data['bedrijfsvoering_en_personeel'] = bool(raw['Bedrijfsvoering en personeel'])
    clean_data['publieke_informatie_en_registratie'] = bool(raw['Publieke informatie en registratie'])
    clean_data['burgerzaken'] = bool(raw['Burgerzaken'])
    clean_data['veiligheid'] = bool(raw['Veiligheid'])
    clean_data['verkeer_en_vervoer'] = bool(raw['Verkeer en vervoer'])
    clean_data['economie'] = bool(raw['Economie'])
    clean_data['onderwijs'] = bool(raw['Onderwijs'])
    clean_data['sport_cultuur_en_recreatie'] = bool(raw['Sport, cultuur en recreatie'])
    clean_data['sociaal_domein'] = bool(raw['Sociaal domein'])
    clean_data['volksgezonheid_en_milieu'] = bool(raw['Volksgezondheid en milieu'])
    clean_data['vhrosv'] = bool(raw['VHROSV'])
    clean_data['heffen_belastingen'] = bool(raw['Heffen belastingen etc'])
    clean_data['alle_taakgebieden'] = bool(raw['Alle taakgebieden'])
    return clean_data


class Command(BaseCommand):
    help = 'Load data from excel file to ProcesType and Resultaat'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        book = open_workbook(file_path)
        sheet = book.sheet_by_index(0)

        for raw in read_xls_row_to_dict(sheet):
            # load to ProcesType
            processtype_data = prepare_procestype(raw)
            # if current nummer already exists - do nothing
            p, created = ProcesType.objects.get_or_create(nummer=processtype_data['nummer'],
                                                          defaults=processtype_data)

            # load to Resultaat
            resultaat_data = prepare_resultaat(raw)
            # if current resultaat already exists - do nothing
            r, created = Resultaat.objects.get_or_create(proces_type=resultaat_data['proces_type'],
                                                         generiek_resultaat=resultaat_data['generiek_resultaat'],
                                                         nummer=resultaat_data['nummer'],
                                                         defaults=resultaat_data)
