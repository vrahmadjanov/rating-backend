from django.db import models
from django.utils.translation import gettext_lazy as _

class Advantage(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название преимущества")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название подписки")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена",
        help_text="Цена в сомони"
    )
    duration_days = models.PositiveIntegerField(
        verbose_name="Длительность (дней)",
        help_text="Сколько дней действует подписка после активации"
    )
    advantages = models.ManyToManyField(
        Advantage,
        related_name='subscriptions',
        verbose_name="Преимущества",
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Доступна ли подписка для покупки"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['price']

    def __str__(self):
        return self.name

    def get_advantages_list(self):
        """Возвращает список названий преимуществ подписки"""
        return list(self.advantages.values_list('name', flat=True))