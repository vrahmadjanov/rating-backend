from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

User = get_user_model()

class Patient(models.Model):
    """
    Модель пациента, связанная с кастомной моделью пользователя (CustomUser).
    """

    # Связь с пользователем
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name=_('Пользователь'),
        help_text=_("Связанный пользователь."),
    )

    # Серия паспорта
    passport = models.CharField(
        _('Серия и номер паспорта'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_("Серия и номер паспорта пациента."),
    )

    # Адрес по прописке
    registration_address = models.CharField(
        _('Адрес по прописке'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Адрес по прописке (город/район)."),
    )

    # Адрес фактического проживания
    actual_address = models.CharField(
        _('Адрес фактического проживания'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Адрес фактического проживания (город/район)."),
    )

    # СИН (Социальный идентификационный номер)
    sin = models.CharField(
        _('СИН'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Социальный идентификационный номер."),
    )

    # ЕНГ (Единый номер гражданина)
    eng = models.CharField(
        _('ЕНГ'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Единый номер гражданина."),
    )

    # Медицинские показатели
    weight = models.DecimalField(
        _('Вес (кг)'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text=_("Вес в килограммах"),
    )
    
    height = models.DecimalField(
        _('Рост (см)'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text=_("Рост в сантиметрах"),
    )
    
    blood_type = models.CharField(
        _('Группа крови'),
        max_length=3,
        blank=True,
        choices=[
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
        ],
        help_text=_("Группа крови и резус-фактор"),
    )

    # Социальный статус пациента
    social_status = models.ForeignKey(
        'SocialStatus',  # Ссылка на модель SocialStatus
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Социальный статус'),
        help_text=_("Социальный статус пациента."),
    )

    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True,
    )
    
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')

    def __str__(self):
        """
        Возвращает строковое представление пациента.
        Формат: "Фамилия Имя Отчество (Пользователь: email)".
        """
        return f"{self.user.get_full_name()} (Пользователь: {self.user.email})"

    def save(self, *args, **kwargs):
        """
        При сохранении автоматически добавляет пользователя в группу 'Patients' (если не добавлен).
        """
        # Сохраняем объект, чтобы убедиться, что он существует в базе данных
        super().save(*args, **kwargs)

        # Добавляем пользователя в группу 'Patients'
        group, _ = Group.objects.get_or_create(name='Patients')
        self.user.groups.add(group)

    @property
    def bmi(self):
        """Рассчитывает и возвращает индекс массы тела (BMI)"""
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None

    def get_age(self):
        """Рассчитывает возраст пациента на основе даты рождения"""
        today = timezone.now().date()
        born = self.user.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))