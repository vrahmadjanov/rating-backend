from django.db import models
from django.contrib.auth import get_user_model
from a_base.models import AcademicDegree, Specialty, MedicalCategory, Service, ExperienceLevel
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Doctor(models.Model):
    """
    Модель врача, содержащая основную информацию о специалисте
    """

    # Связь с пользователем
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
        verbose_name=_("Пользователь"),
        help_text=_("Связанный аккаунт пользователя")
    )

    # Специализация, медицинская категория и ученая степень
    specialties = models.ManyToManyField(
        Specialty,
        blank=True,
        verbose_name=_("Специализации"),
        help_text=_("Основные специализации врача")
    )

    medical_category = models.ForeignKey(
        MedicalCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Медицинская категория"),
        help_text=_("Категория врача (например, высшая, первая)")
    )

    academic_degree = models.ForeignKey(
        AcademicDegree,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Ученая степень"),
        help_text=_("Ученая степень врача (если есть)")
    )

    experience_level = models.ForeignKey(
        ExperienceLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Уровень опыта"),
        help_text=_("Уровень профессионального опыта врача")
    )

    about = models.TextField(
        blank=True,
        verbose_name=_("Краткое описание"),
        help_text=_("Краткое описание своей деятельности")
    )

    # Описание
    philosophy = models.TextField(
        blank=True,
        verbose_name=_("Философия работы"),
        help_text=_("Краткое описание подхода к пациентам")
    )

    # Услуги, которые предоставляет врач
    services = models.ManyToManyField(
        Service,
        blank=True,
        verbose_name=_("Услуги"),
        help_text=_("Медицинские услуги, которые предоставляет врач")
    )

    # Контактная информация
    license_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Номер лицензии"),
        help_text=_("Регистрационный номер лицензии врача")
    )

    # Валидатор для номера телефона (таджикский формат: +992XXYYYYYY)
    phone_regex = RegexValidator(
        regex=r'^\+992\d{9}$',
        message=_("Номер телефона должен быть в формате: '+992XXYYYYYY'."),
    )

    # Поле для номера телефона
    work_phone_number = models.CharField(
        _('Рабочий телефон'),
        validators=[phone_regex],
        max_length=13,
        blank=True,
        null=True,
        help_text=_("Рабочий телефон в формате +992XXYYYYYY.")
    )

    whatsapp = models.CharField(
        _('Номер телефона WhatsApp'),
        validators=[phone_regex],
        max_length=13,
        blank=True,
        null=True,
        help_text=_("Номер телефона для связи через WhatsApp")
    )

    telegram = models.CharField(
        _('Номер телефона или никнейм в Telegram'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Номер телефона или никнейм для связи через Telegram")
    )

    # Звания и заслуги
    titles_and_merits = models.TextField(
        blank=True,
        verbose_name=_("Звания и заслуги"),
        help_text=_("Например: Отличник здравоохранения, член-корреспондент АМН")
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
        help_text=_("Дата и время создания записи")
    )
    
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
        help_text=_("Дата и время последнего обновления записи")
    )

    class Meta:
        verbose_name = _("Врач")
        verbose_name_plural = _("Врачи")
        ordering = ['-created_at']

    def __str__(self):
        """
        Возвращает строковое представление врача: ФИО + специализация.
        """
        user_name = self.user.get_full_name or self.user.email
        specialty_names = ", ".join([s.name for s in self.specialties.all()]) if self.specialties.exists() else _("Без специализации")
        academic_degree = self.academic_degree.name if self.academic_degree else _("Без степени")
        return f"{user_name} ({specialty_names}, {academic_degree})"