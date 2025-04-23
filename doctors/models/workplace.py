from django.db import models
from django.utils.translation import gettext_lazy as _

class Workplace(models.Model):
    """
    Промежуточная модель для связи врача и медицинского учреждения.
    Содержит информацию о должности и периоде работы.
    """

    # Связь с врачом
    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.CASCADE,
        related_name="workplaces",
        verbose_name="Врач",
        help_text="Врач, который работал или работает в этом учреждении"
    )

    # Связь с медицинским учреждением
    medical_institution = models.ForeignKey(
        "MedicalInstitution",
        on_delete=models.CASCADE,
        related_name="workplaces",
        verbose_name="Медицинское учреждение",
        help_text="Медицинское учреждение, где работал или работает врач"
    )

    # Должность врача
    position = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Должность",
        help_text="Должность, которую занимал или занимает врач"
    )

    # Дата начала работы
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата начала работы",
        help_text="Дата, когда врач начал работать в этом учреждении"
    )

    # Дата окончания работы (может быть null, если врач продолжает работать)
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания работы",
        help_text="Дата, когда врач закончил работать в этом учреждении (если продолжает работать, оставьте пустым)"
    )

    class Meta:
        verbose_name = "Место работы"
        verbose_name_plural = "Места работы"
        ordering = ["-start_date"]  # Сортировка по дате начала работы (сначала новые)

    def __str__(self):
        """
        Возвращает строковое представление места работы.
        Формат: "Должность в Название учреждения (Год начала - Год окончания)".
        """
        end_date = self.end_date.strftime("%Y") if self.end_date else "настоящее время"
        return f"{self.doctor.user.email} - {self.position} в {self.medical_institution.name} ({self.start_date.year} - {end_date})"