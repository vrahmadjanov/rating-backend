from django.db import models
from django.utils.translation import gettext_lazy as _

class ExperienceLevel(models.Model):
    """
    Модель для представления уровней опыта врачей
    """

    level = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Уровень опыта"),
        help_text=_("Диапазон лет опыта работы")
    )

    class Meta:
        verbose_name = _("Уровень опыта")
        verbose_name_plural = _("Уровни опыта")
        ordering = ['level']

    def __str__(self):
        return self.level