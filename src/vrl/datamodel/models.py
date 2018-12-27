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
