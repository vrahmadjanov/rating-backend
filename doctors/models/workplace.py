from django.db import models
from clinics.models import Clinic
from .schedule import Schedule
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

    schedule = models.OneToOneField(
        Schedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Расписание",
        help_text="Расписание по дням недели по которому работает врач"
    )

    position = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Должность",
        help_text="Должность, которую занимал или занимает врач"
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата начала работы",
        help_text="Дата, когда врач начал работать в этом учреждении"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания работы",
        help_text="Дата, когда врач закончил работать в этом учреждении (если продолжает работать, оставьте пустым)"
    )

    class Meta:
        verbose_name = "Место работы"
        verbose_name_plural = "Места работы"
        ordering = ["-start_date"]

    def __str__(self):
        """
        Возвращает строковое представление места работы.
        Формат: "Должность в Название учреждения (Год начала - Год окончания)".
        """
        end_date = self.end_date.strftime("%Y") if self.end_date else "настоящее время"
        return f"{self.doctor.user.email} - {self.position} в {self.medical_institution.name} ({self.start_date.year} - {end_date})"