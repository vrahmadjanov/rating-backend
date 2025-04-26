from django.db import models
from django.utils.translation import gettext_lazy as _

class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название специальности"))

    class Meta:
        verbose_name = _("Специальность")
        verbose_name_plural = _("Специальности")

    def __str__(self):
        return self.name