from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from notifications.services import send_email
from map.models import City
from subscriptions.models import Subscription

from django.utils.html import mark_safe
from storages.backends.s3boto3 import S3Boto3Storage

media_storage = S3Boto3Storage()

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель AbstractUser.
    Использует phone_number в качестве логина и добавляет дополнительные поля:
    - ФИО (имя, фамилия, отчество)
    - Номер телефона (в таджикском формате)
    - Email (уникальный адрес э.п.)
    - Фото профиля
    - Пол (мужской/женский)
    - ИНН (индивидуальный номер налогоплательщика)
    """

    # Убираем стандартное поле username, так как используем phone_number для входа
    username = None

    # Валидатор для номера телефона (таджикский формат: +992XXYYYYYY)
    phone_regex = RegexValidator(
        regex=r'^\+992\d{9}$',
        message=_("Номер телефона должен быть в формате: '+992XXYYYYYY'."),
    )

    # Поле для номера телефона
    phone_number = models.CharField(
        _('phone number'),
        validators=[phone_regex],
        max_length=13,
        unique=True,
        help_text=_("Номер телефона в формате +992XXYYYYYY."),
        error_messages={'unique': _("Пользователь с таким номером телефона уже существует.")},
    )

    # Поле email используется для входа в систему
    email = models.EmailField(
        _('email address'),
        null = True,
        blank=True
    )

    # Верифицирован ли email
    email_verified = models.BooleanField(
        _('email verified'),
        default=False,
        help_text=_("Указывает, подтвержден ли email пользователя."),
    )

    # Поля для ФИО (имя, фамилия, отчество)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True, null=True, default='')

    # Дата рождения пользователя
    date_of_birth = models.DateField(
        _('Дата рождения'),
        help_text=_("Дата рождения пользователя."),
    )

    # Поле для фото профиля
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures',
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
        help_text=_("Фотография профиля"),
    )

    # Определяем варианты выбора для поля "пол"
    class Gender(models.TextChoices):
        MALE = 'M', _('Мужской')
        FEMALE = 'F', _('Женский')

    # Поле для выбора пола пользователя
    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=Gender.choices,
        blank=True,
        null=True,
        help_text=_("Пол пользователя (необязательное)."),
    )

    # Поле для ИНН (индивидуальный номер налогоплательщика)
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

    # Город проживания
    city = models.ForeignKey(City, verbose_name="Город проживания", on_delete=models.SET_NULL, null=True)

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

    # Поле, используемое для входа в систему (phone_number вместо username)
    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['first_name', 'date_of_birth']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи') 

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        Формат: "Фамилия Имя Отчество (phone_number)".
        """
        return f"{self.get_full_name()} ({self.phone_number})"
    
    def generate_confirmation_code(self):
        """
        Генерация 6-значного кода подтверждения.
        """
        import random
        self.confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.confirmation_code_created_at = timezone.now()
        self.save()

    def is_confirmation_code_valid(self, code):
        """
        Проверка, что код подтверждения действителен и не истек.
        """
        if self.confirmation_code == code and (timezone.now() - self.confirmation_code_created_at).total_seconds() < 3600:
            return True
        return False
    
    def send_confirmation_email(self):
        """
        Отправка кода подтверждения на email.
        """
        if self.email:
            self.generate_confirmation_code()
            subject = "Подтверждение email"
            message = f"Ваш код подтверждения: {self.confirmation_code}"
            
            # Отправляем email
            if send_email(self.email, subject, message):
                print(f"Код подтверждения отправлен на {self.email}.")
            else:
                print(f"Не удалось отправить код подтверждения на {self.email}.")
        else:
            print("Email не указан. Невозможно отправить код подтверждения.")

    def confirm_email(self, code):
        """
        Подтверждение email с использованием кода подтверждения.
        """
        if self.is_confirmation_code_valid(code):
            self.email_verified = True
            self.save()
            return True
        return False
    
    @property
    def has_active_subscription(self):
        """Проверяет, активна ли подписка пользователя"""
        if not self.subscription:
            return False
        now = timezone.now()
        return self.subscription_end_date and self.subscription_end_date > now
    
    def activate_subscription(self):
        """Активирует подписку для пользователя"""
        duration_days = self.subscription.duration_days
        self.subscription_end_date = self.subscription_start_date + timezone.timedelta(days=duration_days)
        self.save()
    
    def photo_tag(self):
        """
        Возвращает html-объект с фотографией пользователя
        """
        if self.profile_picture:
            return mark_safe(
                '<img src="%s" width="600" />'
                % (self.profile_picture.url)
            )
        return ""

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        Формат: "Фамилия Имя Отчество".
        Если отчество отсутствует, оно не включается в результат.
        """
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))