from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from a_base.models import AppointmentStatus, Gender, CancelReason
from patients.models import Patient
from doctors.models import Doctor
 
class Appointment(models.Model):
    """Модель записи на прием к врачу с встроенным временем приема."""

    # Основные связи
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name="Врач",
        related_name="appointments"
    )
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name="Пациент",
        related_name="appointments"
    )

    # Время приема
    appointment_date = models.DateField(
        verbose_name="Дата приема",
        help_text="Дата на которую назначен прием"
    )
    
    start_time = models.TimeField(
        verbose_name="Время начала",
        help_text="Планируемое время начала приема"
    )
    
    end_time = models.TimeField(
        verbose_name="Время окончания",
        help_text="Планируемое время окончания приема"
    )

    # Статус и отмена
    status = models.ForeignKey(
        AppointmentStatus,
        on_delete=models.CASCADE,
        verbose_name=_("Статус приема"),
        help_text=_("Статус приема")
    )
    
    cancellation_reason = models.ForeignKey(
        CancelReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Причина отмены приема"),
        help_text=_("Причина отмены приема пациентом")
    )
    
    cancellation_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий при отмене",
        max_length=500
    )
    
    cancelled_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Время отмены"
    )

    # Информация о пациенте
    phone_regex = RegexValidator(
        regex=r'^\+992\d{9}$',
        message=_("Формат номера: '+992XXYYYYYY'."),
    )
    
    phone_number = models.CharField(
        _('Телефон'),
        validators=[phone_regex],
        max_length=13,
        help_text=_("Контактный номер пациента")
    )

    # Дополнительная информация
    is_another_patient = models.BooleanField(
        default=False,
        verbose_name="Запись для другого человека"
    )
    
    another_patient_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ФИО другого пациента"
    )
    
    another_patient_age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Возраст",
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    
    another_patient_gender = models.ForeignKey(
        Gender,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Пол пациента"),
        help_text=_("Пол пациента, который записывается на прием")
    )
    
    problem_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание проблемы",
        max_length=1000
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ['appointment_date', 'start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date', 'start_time'],
                name='unique_doctor_time_slot'
            )
        ]

    def __str__(self):
        patient_name = self.another_patient_name if self.is_another_patient else self.patient.user.get_full_name
        return f"{self.appointment_date} {self.start_time}-{self.end_time}: {patient_name} -> {self.doctor}"

    def clean(self):
        """Валидация данных перед сохранением."""
        from django.core.exceptions import ValidationError
        
        # Проверка времени
        if self.start_time >= self.end_time:
            raise ValidationError("Время окончания должно быть позже времени начала")
            
        # Проверка для записи другого человека
        if self.is_another_patient and not self.another_patient_name:
            raise ValidationError("Укажите ФИО пациента при записи другого человека")
            
        # Проверка причины отмены
        if self.status == AppointmentStatus.objects.get(name_ru="Отменен") and not self.cancellation_reason:
            raise ValidationError("Укажите причину отмены записи")
            
        if self.cancellation_reason == CancelReason.objects.get(name_ru="Другое") and not self.cancellation_notes:
            raise ValidationError("Укажите детали причины при выборе 'Другое'")

    def cancel(self, by_patient=None, reason=None, notes=None):
        """Метод для отмены записи."""
        if self.status == AppointmentStatus.objects.get(name_ru="Отменен"):
            raise ValueError("Запись уже отменена")
            
        self.status = AppointmentStatus.objects.get(name_ru="Отменен")
        self.cancellation_reason = reason
        self.cancellation_notes = notes
        self.cancelled_at = timezone.now()
        self.save()

    def complete(self):
        """Метод для отметки о завершении приема."""
        self.status = AppointmentStatus.objects.get(name_ru="Завершен")
        self.save()

    def reschedule(self, new_date, new_start, new_end):
        """Метод для переноса записи."""
        self.appointment_date = new_date
        self.start_time = new_start
        self.end_time = new_end
        self.save()

    @property
    def is_upcoming(self):
        """Проверяет, является ли запись предстоящей."""
        now = timezone.now()
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.appointment_date, self.start_time)
        )
        return self.status == AppointmentStatus.objects.get(name_ru="Предстоящий") and appointment_datetime > now