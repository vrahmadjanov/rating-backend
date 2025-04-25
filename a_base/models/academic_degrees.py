from django.db import models
from django.utils.translation import gettext_lazy as _

class AcademicDegree(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Название учёной степени"))

    class Meta:
        verbose_name = _("Научная степень")
        verbose_name_plural = _("Научные степени")
        ordering = ['name']

    def __str__(self):
        return self.name