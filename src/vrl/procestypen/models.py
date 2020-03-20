import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProcesType(models.Model):
    uuid = models.UUIDField(_("uuid"), default=uuid.uuid4)

    nummer = models.PositiveSmallIntegerField(
        _("procestypenummer"),
        unique=True,
        help_text=_("Nummer van de selectielijstcategorie"),
    )
    naam = models.CharField(
        _("procestypenaam"), max_length=40, help_text=_("Benaming van het procestype")
    )
    omschrijving = models.CharField(
        _("procestypeomschrijving"),
        max_length=80,
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
