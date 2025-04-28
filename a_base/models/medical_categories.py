from django.db import models
from django.utils.translation import gettext_lazy as _

class MedicalCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название медицинской категории"))

    class Meta:
        verbose_name = _("Медицинская категория")
        verbose_name_plural = _("Медицинские категории")

    def __str__(self):
        return self.name