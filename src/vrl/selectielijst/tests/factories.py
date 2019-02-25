import factory
import factory.fuzzy

from ..constants import ArchiefNominaties


class ProcesTypeFactory(factory.django.DjangoModelFactory):
    nummer = factory.Sequence(lambda n: n)
    naam = factory.Faker('bs')
    omschrijving = factory.Faker('text')
    toelichting = factory.Faker('text')
    procesobject = factory.Faker('bs')

    class Meta:
        model = 'selectielijst.ProcesType'


class ResultaatFactory(factory.django.DjangoModelFactory):
    proces_type = factory.SubFactory(ProcesTypeFactory)

    nummer = factory.Sequence(lambda n: n)
    naam = factory.fuzzy.FuzzyText(length=40)
    herkomst = factory.fuzzy.FuzzyChoice(['Risicoanalyse', 'Systeemanalyse'])
    waardering = factory.fuzzy.FuzzyChoice(ArchiefNominaties.values)

    class Meta:
        model = 'selectielijst.Resultaat'
