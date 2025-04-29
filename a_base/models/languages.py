from django.db import models
from django.utils.translation import gettext_lazy as _

class Language(models.Model):
    """
    Модель для хранения информации о языках.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Язык"),
        help_text=_("Название языка"),
        unique=True
    )

    class Meta:
        verbose_name = _("Язык")
        verbose_name_plural = _("Языки")

    def __str__(self):
        return self.name

class LanguageLevel(models.Model):
    """
    Модель для хранения информации об уровнях владения языком.
    """
    level = models.CharField(
        max_length=100,
        verbose_name=_("Уровень владения"),
        help_text=_("Уровень владения языком"),
        unique=True
    )

    class Meta:
        verbose_name = _("Уровень владения языком")
        verbose_name_plural = _("Уровни владения языками")

    def __str__(self):
        return self.level