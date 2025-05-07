from django.db import models
from django.utils.translation import gettext_lazy as _

class CancelReason(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название причины отмены записи"))

    class Meta:
        verbose_name = _("Причина отмены записи")
        verbose_name_plural = _("Причины отмены записи")

    def __str__(self):
        return self.name