from django.db import models
from django.utils.translation import gettext_lazy as _

class ClinicType(models.Model):
    """
    Типы клиник
    """

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название типа клиники"))

    class Meta:
        verbose_name = _("Тип клиники")
        verbose_name_plural = _("Типы клиник")
        ordering = ["name"]

    def __str__(self):
        return self.name