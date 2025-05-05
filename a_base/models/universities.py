from django.db import models
from django.utils.translation import gettext_lazy as _

class University(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название вуза"))
    city = models.CharField(max_length=255, verbose_name=_("Город, где находится вуз"))
    country = models.CharField(max_length=255, verbose_name=_("Страна, где находится вуз"))

    class Meta:
        verbose_name = _("Вуз")
        verbose_name_plural = _("Вузы")

    def __str__(self):
        return self.name