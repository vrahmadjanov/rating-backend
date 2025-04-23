from django.db import models
from django.utils.translation import gettext_lazy as _

class Region(models.Model):
    """
    Модель для хранения информации об областях.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Название области",
        help_text="Название области (например, Согдийская область)"
    )

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"
        ordering = ["name"]

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Модель для хранения информации о городах/районах.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Название города/района",
        help_text="Название города или района (например, Душанбе)"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name="Область",
        help_text="Область, к которой принадлежит город/район"
    )

    class Meta:
        verbose_name = "Город/Район"
        verbose_name_plural = "Города/Районы"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.region}"