from django.db import models
from django.utils.translation import gettext_lazy as _

class Region(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100, verbose_name=_("Название региона"))

    class Meta:
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.id})"

class District(models.Model):
    code = models.CharField(max_length=2, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=_("Название района"))
    region = models.ForeignKey(Region, verbose_name=_("Регион"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Район")
        verbose_name_plural = _("Районы")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code}) | {self.region.name}"