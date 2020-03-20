import factory


class CommunicatieKanaalFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")
    omschrijving = factory.Faker("bs")

    class Meta:
        model = "datamodel.CommunicatieKanaal"
        django_get_or_create = ("naam",)
