from django.db import models
from django.utils.translation import gettext_lazy as _
from .doctors import Doctor
from a_base.models import University

class Education(models.Model):
    """
    Модель для хранения информации об образовании врача.
    Содержит данные о вузе и годе окончания.
    """

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name=_("Врач"),
        help_text=_("Врач, к которому относится это образование")
    )

    university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name=_("Университет"),
        help_text=_("Университет, в котором доктор получил образование")
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
        return f"{self.doctor.user.get_full_name} | {self.university.name} ({self.graduation_year})"