from django.db import models
from django.utils.translation import gettext_lazy as _

class AppointmentStatus(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название статуса записи"))

    class Meta:
        verbose_name = _("Статус записи")
        verbose_name_plural = _("Статусы записей")

    def __str__(self):
        return self.name