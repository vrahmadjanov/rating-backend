from django.db import models
from clinics.models import Clinic
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Workplace(models.Model):
    """
    Промежуточная модель для связи врача и медицинского учреждения.
    Содержит информацию о должности и периоде работы.
    """

    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.CASCADE,
        related_name="workplaces",
        verbose_name="Врач",
        help_text="Врач, который работал или работает в этом учреждении"
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name="workplaces",
        verbose_name="Медицинское учреждение",
        help_text="Медицинское учреждение, где работал или работает врач"
    )

    position = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Должность",
        help_text="Должность, которую занимал или занимает врач"
    )

    monday_start = models.TimeField(verbose_name="Понедельник - начало",blank=True, null=True)
    monday_end = models.TimeField(verbose_name="Понедельник - конец", blank=True, null=True)
    tuesday_start = models.TimeField(verbose_name="Вторник - начало", blank=True, null=True)
    tuesday_end = models.TimeField(verbose_name="Вторник - конец", blank=True, null=True)
    wednesday_start = models.TimeField(verbose_name="Среда - начало", blank=True, null=True)
    wednesday_end = models.TimeField(verbose_name="Среда - конец", blank=True, null=True)
    thursday_start = models.TimeField(verbose_name="Четверг - начало", blank=True, null=True)
    thursday_end = models.TimeField(verbose_name="Четверг - конец", blank=True, null=True)
    friday_start = models.TimeField(verbose_name="Пятница - начало", blank=True, null=True)
    friday_end = models.TimeField(verbose_name="Пятница - конец", blank=True, null=True)
    saturday_start = models.TimeField(verbose_name="Суббота - начало", blank=True, null=True)
    saturday_end = models.TimeField(verbose_name="Суббота - конец", blank=True, null=True)
    sunday_start = models.TimeField(verbose_name="Воскресенье - начало", blank=True, null=True)
    sunday_end = models.TimeField(verbose_name="Воскресенье - конец", blank=True, null=True)

    appointment_interval = models.PositiveSmallIntegerField(
        verbose_name="Интервал приема",
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(360)],
        help_text="Длительность одного приема пациента в минутах (15-360)"
    )

    class Meta:
        verbose_name = "Место работы"
        verbose_name_plural = "Места работы"

    def __str__(self):
        """
        Возвращает строковое представление места работы.
        """
        return f"{self.doctor.user.get_full_name} - {self.position} в {self.clinic.name}"