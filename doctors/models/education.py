from django.db import models
from django.utils.translation import gettext_lazy as _
from .doctors import Doctor

class Education(models.Model):
    """
    Модель для хранения информации об образовании врача.
    Содержит данные о вузе, городе, стране и годе окончания.
    """

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name=_("Врач"),
        help_text=_("Врач, к которому относится это образование")
    )

    institution_name = models.CharField(
        max_length=255,
        verbose_name=_("Название вуза"),
        help_text=_("Название учебного заведения")
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_("Город"),
        help_text=_("Город, где находится учебное заведение")
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_("Страна"),
        help_text=_("Страна, где находится учебное заведение")
    )

    graduation_year = models.PositiveIntegerField(
        verbose_name=_("Год окончания"),
        help_text=_("Год окончания учебного заведения")
    )

    class Meta:
        verbose_name = _("Образование")
        verbose_name_plural = _("Образования")
        ordering = ["-graduation_year"]  # Сортировка по году окончания (сначала новые)

    def __str__(self):
        """
        Возвращает строковое представление образования.
        Формат: "Название вуза, Город, Страна (Год окончания)".
        """
        return f"{self.institution_name}, {self.city}, {self.country} ({self.graduation_year})"