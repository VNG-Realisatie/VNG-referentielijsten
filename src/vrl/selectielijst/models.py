import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from relativedeltafield import RelativeDeltaField
from vng_api_common.constants import Archiefnominatie

from .constants import Procestermijnen
from .query import ResultaatQuerySet


class ProcesType(models.Model):
    uuid = models.UUIDField(_("uuid"), default=uuid.uuid4)

    nummer = models.PositiveSmallIntegerField(
        _("procestypenummer"),
        unique=True,
        help_text=_("Nummer van de selectielijstcategorie"),
    )
    naam = models.CharField(
        _("procestypenaam"), max_length=100, help_text=_("Benaming van het procestype")
    )
    omschrijving = models.CharField(
        _("procestypeomschrijving"),
        max_length=300,
        help_text=_("Omschrijving van het procestype"),
    )
    toelichting = models.TextField(
        _("procestypetoelichting"), help_text=_("Toelichting van het procestype")
    )
    procesobject = models.CharField(
        _("procesobject"),
        max_length=80,
        help_text=_(
            "Object waar de uitvoering van het proces op van toepassing is en waarvan de "
            "bestaans- of geldigheidsduur eventueel van belang is bij het bepalen van de "
            "start van de bewaartermijn"
        ),
    )

    class Meta:
        verbose_name = _("procestype")
        verbose_name_plural = _("procestypen")

    def __str__(self):
        return f"{self.nummer} - {self.naam}"


class Resultaat(models.Model):
    uuid = models.UUIDField(_("uuid"), default=uuid.uuid4)

    # relations/tree
    # The tree is modelled via a simple self-FK because it cannot have arbitrary depth
    proces_type = models.ForeignKey(
        "ProcesType", on_delete=models.CASCADE, verbose_name=_("procestype")
    )
    generiek_resultaat = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"generiek_resultaat__isnull": True},
        verbose_name=_("generiek resultaat"),
        help_text=_(
            "Voor specifieke resultaten, geef aan bij welk generiek resultaat deze hoort"
        ),
    )

    nummer = models.PositiveSmallIntegerField(
        _("nummer"),
        help_text=_(
            "Nummer van het resultaat. Dit wordt samengesteld met het procestype en "
            "generiek resultaat indien van toepassing."
        ),
    )
    naam = models.CharField(
        _("naam"), max_length=40, help_text=_("Benaming van het procestype")
    )
    omschrijving = models.CharField(
        _("omschrijving"),
        max_length=150,
        blank=True,
        help_text=_("Omschrijving van het specifieke resultaat"),
    )
    herkomst = models.CharField(
        _("herkomst"),
        max_length=200,
        help_text=_(
            "Voorbeeld: 'Risicoanalyse', 'Systeemanalyse' of verwijzing naar Wet- en regelgeving"
        ),
    )
    waardering = models.CharField(
        _("waardering"), max_length=50, choices=Archiefnominatie.choices
    )
    procestermijn = models.CharField(
        _("procestermijn"), max_length=50, choices=Procestermijnen.choices, blank=True
    )
    bewaartermijn = RelativeDeltaField(_("bewaartermijn"), null=True, blank=True)
    toelichting = models.TextField(_("toelichting"), blank=True)

    # relevant domains
    algemeen_bestuur_en_inrichting_organisatie = models.BooleanField(
        _("algemeen bestuur en inrichting organisatie"), default=False
    )
    bedrijfsvoering_en_personeel = models.BooleanField(
        _("bedrijfsvoering en personeel"), default=False
    )
    publieke_informatie_en_registratie = models.BooleanField(
        _("publieke informatie en registratie"), default=False
    )
    burgerzaken = models.BooleanField(_("burgerzaken"), default=False)
    veiligheid = models.BooleanField(_("veiligheid"), default=False)
    verkeer_en_vervoer = models.BooleanField(_("verkeer en vervoer"), default=False)
    economie = models.BooleanField(_("economie"), default=False)
    onderwijs = models.BooleanField(_("onderwijs"), default=False)
    sport_cultuur_en_recreatie = models.BooleanField(
        _("sport, cultuur en recreatie"), default=False
    )
    sociaal_domein = models.BooleanField(_("sociaal domein"), default=False)
    volksgezonheid_en_milieu = models.BooleanField(
        _("volksgezonheid en milieu"), default=False
    )
    vhrosv = models.BooleanField(_("VHROSV"), default=False)
    heffen_belastingen = models.BooleanField(
        _("heffen belastingen etc."), default=False
    )
    alle_taakgebieden = models.BooleanField(_("alle taakgebieden"), default=False)
    procestermijn_opmerking = models.CharField(
        _("procestermijn opmerking"),
        max_length=20,
        blank=True,
        help_text=_("Voorbeeld: '25 jaar', '30 jaar, '5 of 10 jaar'"),
    )

    objects = ResultaatQuerySet.as_manager()

    class Meta:
        verbose_name = _("resultaat")
        verbose_name_plural = _("resultaten")
        unique_together = ("proces_type", "generiek_resultaat", "nummer")

    def __str__(self):
        return f"{self.volledig_nummer} - {self.naam}"

    def clean(self):
        super().clean()

        if self.specifiek:
            if not self.omschrijving:
                raise ValidationError(
                    {
                        "omschrijving": _(
                            "Omschrijving is een verplicht veld voor specifieke resultaten"
                        )
                    },
                    code="required",
                )
            if self.proces_type_id != self.generiek_resultaat.proces_type_id:
                raise ValidationError(
                    {
                        "proces_type": _(
                            "Het procestype moet hetzelfde zijn als het procestype van het "
                            "generiek resultaat."
                        )
                    },
                    code="invalid",
                )
        elif self.generiek and self.omschrijving:
            raise ValidationError(
                {
                    "omschrijving": _(
                        "Omschrijving mag niet opgegeven worden voor generieke resultaten"
                    )
                },
                code="forbidden",
            )

    @property
    def generiek(self) -> bool:
        return self.generiek_resultaat_id is None

    @property
    def specifiek(self) -> bool:
        return not self.generiek

    @property
    def volledig_nummer(self) -> str:
        """
        Calculate the complete number of the result.
        """
        generiek_resultaat_nr = (
            f".{self.generiek_resultaat.nummer}" if self.specifiek else ""
        )
        return f"{self.proces_type.nummer}{generiek_resultaat_nr}.{self.nummer}"
