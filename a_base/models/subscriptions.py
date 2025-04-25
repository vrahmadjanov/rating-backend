from django.db import models
from django.utils.translation import gettext_lazy as _

class Advantage(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Название преимущества"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Преимущество")
        verbose_name_plural = _("Преимущества")

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Название подписки"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Цена"),
        help_text=_("Цена в сомони")
    )
    duration_days = models.PositiveIntegerField(
        verbose_name=_("Длительность (дней)"),
        help_text=_("Сколько дней действует подписка после активации")
    )
    advantages = models.ManyToManyField(
        Advantage,
        related_name='subscriptions',
        verbose_name=_("Преимущества"),
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активна"),
        help_text=_("Доступна ли подписка для покупки")
    )

    class Meta:
        verbose_name = _("Подписка")
        verbose_name_plural = _("Подписки")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_advantages_list(self):
        """Возвращает список названий преимуществ подписки"""
        return list(self.advantages.values_list('name', flat=True))