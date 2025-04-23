from django.db import models
from appointments.models import Appointment
from django.utils.translation import gettext_lazy as _

class Visit(models.Model):
    """
    Модель для хранения информации о посещениях пациента к врачу.
    Одно посещение может быть связано только с одной записью.
    """

    # Связь с записью, если визит был по записи
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="visit",
        verbose_name="Запись на приём",
        help_text="Запись пациента на приём (если визит был по записи)"
    )

    # Дата и время визита
    visit_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время визита",
        help_text="Время, когда пациент пришёл на приём"
    )

    # Заключение врача
    diagnosis = models.TextField(
        null=True,
        blank=True,
        verbose_name="Диагноз",
        help_text="Заключение или диагноз, поставленный врачом"
    )

    # Назначения (лекарства, процедуры)
    prescriptions = models.TextField(
        null=True,
        blank=True,
        verbose_name="Назначения",
        help_text="Назначения врача: лекарства, процедуры, рекомендации"
    )

    # Статус визита (например, завершён, отменён)
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name="Статус визита",
        help_text="Статус визита"
    )

    # Примечания
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Примечания",
        help_text="Дополнительные примечания для визита"
    )

    # Анамнез пациента (необязательное поле)
    anamnesis = models.TextField(
        null=True,
        blank=True,
        verbose_name="Анамнез",
        help_text="Информация об анамнезе пациента (необязательное поле)"
    )

    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"

    def __str__(self):
        """
        Возвращает строковое представление визита.
        Формат: "Пациент: Дата и время визита"
        """
        return f"{self.patient.user.get_full_name()} - {self.visit_time.strftime('%Y-%m-%d %H:%M')}"
    
    def get_doctor(self):
        """
        Получить врача через расписание.
        """
        return self.appointment.slot.schedule.workplace.doctor
    
    def get_patient(self):
        """
        Получить пациента через запись.
        """
        return self.appointment.patient
