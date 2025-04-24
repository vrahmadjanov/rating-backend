from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from a_base.models import Region, District


class MedicalInstitution(models.Model):
    """
    Модель для хранения информации о медицинском учреждении.
    Содержит данные о названии, адресе, типе учреждения, координатах и других стандартных полях.
    """

    # Название медицинского учреждения
    name = models.CharField(
        max_length=255,
        verbose_name="Название учреждения",
        help_text="Официальное название медицинского учреждения"
    )

    # Тип медицинского учреждения
    class InstitutionType(models.TextChoices):
        HOSPITAL = "HOSPITAL", _("Госпитальная служба")
        PRIMARY_CARE = "PRIMARY_CARE", _("Учреждение ПМСП")

    # Тип учреждения
    institution_type = models.CharField(
        max_length=50,
        choices=InstitutionType.choices,
        verbose_name="Тип учреждения",
        help_text="Тип медицинского учреждения (Госпитальная служба или Учреждение ПМСП)"
    )

    # Адрес учреждения
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес",
        help_text="Адрес медицинского учреждения"
    )

    # Страна
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        help_text="Страна, где находится медицинское учреждение",
        default="Таджикистан"
    )

    # Область
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name="Область",
        help_text="Область, в которой находится медицинское учреждение"
    )

    # Район
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        verbose_name="Район",
        help_text="Район, где находится медицинское учреждение"
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
        help_text=_("Контактный номер медицинского учреждения"),
    )

    # Электронная почта
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Электронная почта",
        help_text="Электронная почта учреждения"
    )

    # Веб-сайт
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name="Веб-сайт",
        help_text="Официальный веб-сайт учреждения"
    )

    # Широта
    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Широта",
        help_text="Географическая широта местоположения учреждения"
    )

    # Долгота
    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Долгота",
        help_text="Географическая долгота местоположения учреждения"
    )

    class Meta:
        verbose_name = "Медицинское учреждение"
        verbose_name_plural = "Медицинские учреждения"
        ordering = ["name"]

    def __str__(self):
        """
        Возвращает строковое представление медицинского учреждения.
        Формат: "Город/Район, Название учреждения, Тип учреждения, Адрес".
        """
        return f"{self.city.name}, {self.name}, {self.get_institution_type_display()}, {self.address}"