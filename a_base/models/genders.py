from django.db import models
from django.utils.translation import gettext_lazy as _

class Gender(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Пол"))

    class Meta:
        verbose_name = _("Пол")
        verbose_name_plural = _("Пол")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}"
