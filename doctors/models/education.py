from django.db import models
from .doctors import Doctor

class Education(models.Model):
    """
    Модель для хранения информации об образовании врача.
    Содержит данные о вузе, городе, стране и годе окончания.
    """

    # Связь с врачом
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name="Врач",
        help_text="Врач, к которому относится это образование"
    )

    # Название вуза
    institution_name = models.CharField(
        max_length=255,
        verbose_name="Название вуза",
        help_text="Название учебного заведения"
    )

    # Город вуза
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Город, где находится учебное заведение"
    )

    # Страна вуза
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        help_text="Страна, где находится учебное заведение"
    )

    # Год окончания
    graduation_year = models.PositiveIntegerField(
        verbose_name="Год окончания",
        help_text="Год окончания учебного заведения"
    )

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образования"
        ordering = ["-graduation_year"]  # Сортировка по году окончания (сначала новые)

    def __str__(self):
        """
        Возвращает строковое представление образования.
        Формат: "Название вуза, Город, Страна (Год окончания)".
        """
        return f"{self.institution_name}, {self.city}, {self.country} ({self.graduation_year})"