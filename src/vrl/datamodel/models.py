import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CommunicatieKanaal(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4,
        help_text="Unieke resource identifier (UUID4)"
    )
    naam = models.CharField(
        _("naam"), max_length=20, unique=True,
        help_text=_("De gangbare naam van het communicatiekanaal.")
    )
    omschrijving = models.TextField(
        _("omschrijving"), max_length=200,
        help_text=_("Toelichtende beschrijving van (de naam van) het communicatiekanaal.")
    )

    class Meta:
        verbose_name = _("communicatiekanaal")
        verbose_name_plural = _("communicatiekanalen")

    def __str__(self):
        return self.naam


class ResultaattypeOmschrijvingGeneriek(models.Model):
    """
    Algemeen gehanteerde omschrijvingen van de aard van resultaten van zaken.

    Bron: https://www.gemmaonline.nl/index.php/Imztc_2.2/doc/referentielijst/resultaattype-omschrijving_generiek

    Begin/eind geldigheid are left out because they are tightly coupled with
    dates in a ZTC, while we're decoupling stuff here.

    Herkomst is left out, because in the common-ground vision of 'data bij de
    bron', you do NOT copy/pump data around.
    """
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4,
        help_text="Unieke resource identifier (UUID4)"
    )
    omschrijving = models.CharField(
        _("omschrijving"), max_length=20,
        help_text=_("Algemeen gehanteerde omschrijvingen van de aard van het resultaat van zaken")
    )
    definitie = models.TextField(
        _("definitie"), max_length=255,
        help_text=_("Nauwkeurige beschrijving van het generieke type resultaat.")
    )
    opmerking = models.TextField(
        _("opmerking"), max_length=255, blank=True,
        help_text=_("Zinvolle toelichting bij de waarde van de generieke omschrijving van het resultaat.")
    )

    class Meta:
        verbose_name = _("generieke resultaattypeomschrijving")
        verbose_name_plural = _("generieke resultaattypeomschrijvingen")

    def __str__(self):
        return self.omschrijving
