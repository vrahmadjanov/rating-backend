from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractUser
from a_base.models import District
from a_base.models import Subscription

from .managers import CustomUserManager
from storages.backends.s3boto3 import S3Boto3Storage

media_storage = S3Boto3Storage()

class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    class Gender(models.TextChoices):
        MALE = 'M', _('Мужской')
        FEMALE = 'F', _('Женский')
    
    # Валидатор для номера телефона
    phone_regex = RegexValidator(
        regex=r'^\+992\d{9}$',
        message=_("Номер телефона должен быть в формате: '+992XXYYYYYY'."),
    )

    username = None

    # Персональные данные
    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150)
    middle_name = models.CharField(_('Отчество'), max_length=150, blank=True, null=True)
    
    date_of_birth = models.DateField(
        _('Дата рождения'),
        help_text=_("Дата рождения пользователя."),
    )

    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=Gender.choices,
        blank=True,
        null=True,
        help_text=_("Пол пользователя (необязательное)."),
    )

    district = models.ForeignKey(District, verbose_name="Район проживания пользователя", on_delete=models.SET_NULL, null=True)

    phone_number = models.CharField(
        _('Номер телефона'),
        validators=[phone_regex],
        max_length=13,
        unique=True,
        help_text=_("Номер телефона в формате +992XXYYYYYY."),
        error_messages={'unique': _("Пользователь с таким номером телефона уже существует.")},
    )

    email = models.EmailField(
        _('Электронная почта'),
        null = True,
        blank=True
    )

    profile_picture = models.ImageField(
        _('Фотография профиля'),
        upload_to='profile_pictures',
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
        help_text=_("Фотография профиля"),
    )

    email_verified = models.BooleanField(
        _('Электронная почта подтверждена'),
        default=False,
        help_text=_("Указывает, подтвержден ли email пользователя."),
    )

    # Индивидуальный номер налогоплательщика
    inn = models.CharField(
        _('ИНН'),
        max_length=9,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(regex=r'^\d{9}$', message=_("ИНН должен состоять из 9 цифр.")),
            MinLengthValidator(9),
            MaxLengthValidator(9),
        ],
        help_text=_("Индивидуальный номер налогоплательщика (9 цифр)."),
        error_messages={'unique': _("Пользователь с таким ИНН уже существует.")},
    )

    # Подписка
    subscription = models.ForeignKey(
        Subscription, 
        verbose_name="Подписка", 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    subscription_start_date = models.DateTimeField(blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)

    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmation_code_created_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['first_name', 'date_of_birth']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи') 

    def __str__(self):
        return f"{self.get_full_name} ({self.phone_number})"
    
    def generate_confirmation_code(self):
        """Генерирует код подтверждения"""
        import random
        self.confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.confirmation_code_created_at = timezone.now()
        self.save()

    def is_confirmation_code_valid(self, code):
        """Проверяет код подтверждения"""
        if self.confirmation_code == code and (timezone.now() - self.confirmation_code_created_at).total_seconds() < 3600:
            return True
        return False
    
    def activate_subscription(self):
        """Активирует подписку для пользователя"""
        duration_days = self.subscription.duration_days
        self.subscription_end_date = self.subscription_start_date + timezone.timedelta(days=duration_days)
        self.save()

    @property
    def has_active_subscription(self):
        """Проверяет, активна ли подписка пользователя"""
        if not self.subscription:
            return False
        now = timezone.now()
        return self.subscription_end_date and self.subscription_end_date > now

    @property
    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))