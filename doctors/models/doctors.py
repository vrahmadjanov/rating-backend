from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Avg
from .specialty import Specialty
from .medical_category import MedicalCategory
from .service import Service
from .academic_degree import AcademicDegree
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Doctor(models.Model):
    """
    Модель врача, содержащая основную информацию о специалисте:
    - Связь с пользователем
    - Специализация, категория и ученая степень
    - Образование
    - Места работы
    - Описание деятельности
    - Описание работы c пациентами
    - Услуги, которые предоставляет врач
    - Верификация
    - Звания и заслуги
    - Знание языков
    - Контакты
    """

    # Связь с пользователем
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
        verbose_name="Пользователь"
    )

    # Специализация, медицинская категория и ученая степень
    specialty = models.ManyToManyField(
        Specialty,
        null=True,
        blank=True,
        verbose_name="Специализации",
        help_text="Основные специализации врача"
    )

    medical_category = models.ForeignKey(
        MedicalCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Медицинская категория",
        help_text="Категория врача (например, высшая, первая)"
    )

    academic_degree = models.ForeignKey(
        AcademicDegree,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ученая степень",
        help_text="Ученая степень врача (если есть)"
    )

    class ExperienceChoices(models.TextChoices):
        JUNIOR = '0-3', '0-3 года'
        MIDDLE = '4-10', '4-10 лет'
        SENIOR = '11-20', '11-20 лет'
        EXPERT = '20+', 'Более 20 лет'

    experience_years = models.CharField(
        max_length=7,
        null = True,
        choices=ExperienceChoices.choices,
        verbose_name="Стаж работы",
        help_text="Общий стаж работы врача"
    )

    about = models.TextField(
        blank=True,
        null=True,
        verbose_name="Краткое описание",
        help_text="Краткое описание своей деятельности"
    )

    # Описание
    philosophy = models.TextField(
        blank=True,
        null=True,
        verbose_name="Философия работы",
        help_text="Краткое описание подхода к пациентам"
    )

    # Услуги, которые предоставляет врач
    services = models.ManyToManyField(
        Service,
        blank=True,
        verbose_name="Услуги",
        help_text="Медицинские услуги, которые предоставляет врач"
    )

    # Контактная информация
    license_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Номер лицензии",
        help_text="Регистрационный номер лицензии врача"
    )

    # Валидатор для номера телефона (таджикский формат: +992XXYYYYYY)
    phone_regex = RegexValidator(
        regex=r'^\+992\d{9}$',
        message=_("Номер телефона должен быть в формате: '+992XXYYYYYY'."),
    )

    # Поле для номера телефона
    work_phone_number = models.CharField(
        _('phone number'),
        validators=[phone_regex],
        max_length=13,
        help_text=_("Рабочий телефон в формате +992XXYYYYYY."),
    )

    whatsapp = models.CharField(
        _('Номер телефона WhatsApp'),
        validators=[phone_regex],
        blank=True,
        null=True,
        help_text="Номер телефона для связи через WhatsApp"
    )

    telegram = models.CharField(
        _('Номер телефона Telegram'),
        validators=[phone_regex],
        blank=True,
        null=True,
        help_text="Номер телефона для связи через Telegram"
    )

    # Верификация
    is_verified = models.BooleanField(
        default=True,
        verbose_name="Верифицирован",
        help_text="Флаг, указывающий, верифицирован ли врач"
    )

    verification_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата верификации",
        help_text="Дата прохождения верификации"
    )

    verified_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Кем верифицирован",
        help_text="Имя администратора, который провел верификацию"
    )

    # Звания и заслуги
    titles_and_merits = models.TextField(
        blank=True,
        null=True,
        verbose_name="Звания и заслуги",
        help_text="Например: Отличник здравоохранения, член-корреспондент АМН"
    )

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        """
        Возвращает строковое представление врача: ФИО + специализация.
        """
        user_name = self.user.get_full_name or self.user.email
        specialty_name = self.specialty.name if self.specialty else "Без специализации"
        academic_degree = self.academic_degree or "Без степени"
        return f"{user_name} ({specialty_name}, {academic_degree})"