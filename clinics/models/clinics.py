from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from a_base.models import District
from clinics.models import ClinicType


class Clinic(models.Model):
    """
    Модель для хранения информации о клинике.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_("Название клиники"),
        help_text=_("Официальное название клиники")
    )

    clinic_type = models.ForeignKey(
        ClinicType,
        on_delete=models.PROTECT,
        verbose_name=_("Тип клиники"),
        help_text=_("Тип клиники (Госпитальная служба или Учреждение ПМСП)")
    )

    address = models.CharField(
        max_length=255,
        verbose_name=_("Адрес"),
        help_text=_("Адрес клиники")
    )

    # Страна
    country = models.CharField(
        max_length=100,
        verbose_name=_("Страна"),
        help_text=_("Страна, где находится клиника"),
        default="Таджикистан"
    )

    # Район
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        verbose_name=_("Район"),
        help_text=_("Район, где находится клиника")
    )

    phone_regex = RegexValidator(
        regex=r'^\+992\d{9}$',
        message=_("Номер телефона должен быть в формате: '+992XXYYYYYY'."),
    )

    # Поле для номера телефона
    phone_number = models.CharField(
        _('Контактный телефон'),
        validators=[phone_regex],
        max_length=13,
        blank=True,
        null=True,
        help_text=_("Контактный номер клиники"),
    )

    # Электронная почта
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Электронная почта"),
        help_text=_("Электронная почта клиники")
    )

    # Веб-сайт
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Веб-сайт"),
        help_text=_("Официальный веб-сайт клиники")
    )

    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("Широта"),
        help_text=_("Географическая широта местоположения клиники")
    )

    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("Долгота"),
        help_text=_("Географическая долгота местоположения клиники")
    )

    class Meta:
        verbose_name = _("Клиника")
        verbose_name_plural = _("Клиники")
        ordering = ["name"]

    def __str__(self):
        """
        Возвращает строковое представление медицинского учреждения.
        Формат: "Район, Название учреждения, Тип учреждения, Адрес".
        """
        return f"{self.district.name}, {self.name}, {self.clinic_type}, {self.address}"