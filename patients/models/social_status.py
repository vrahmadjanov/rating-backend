from django.db import models
from django.utils.translation import gettext_lazy as _

class SocialStatus(models.Model):
    """
    Модель для хранения социальных статусов пациентов.
    """

    name = models.CharField(
        _('Название'),
        max_length=50,
        unique=True,
        help_text=_("Название социального статуса (например, 'Студент', 'Пенсионер')."),
    )

    description = models.TextField(
        _('Описание'),
        blank=True,
        null=True,
        help_text=_("Краткое описание социального статуса."),
    )

    class Meta:
        verbose_name = _('Социальный статус')
        verbose_name_plural = _('Социальные статусы')

    def __str__(self):
        """
        Возвращает строковое представление социального статуса.
        """
        return self.name