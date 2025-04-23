from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Review(models.Model):
    """
    Модель для хранения отзывов о приемах у врача
    """
    appointment = models.OneToOneField(
        'Appointment',
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name=_('Запись на прием'),
        help_text=_('Запись на прием, к которой относится отзыв')
    )
    
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    
    rating = models.PositiveSmallIntegerField(
        _('Оценка'),
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Оценка от 1 до 5')
    )
    
    comment = models.TextField(
        _('Комментарий'),
        blank=True,
        null=True,
        max_length=2000,
        help_text=_('Текст отзыва (максимум 2000 символов)')
    )
    
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True,
        help_text=_('Дата и время создания отзыва')
    )
    
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True,
        help_text=_('Дата и время последнего обновления отзыва')
    )
    
    is_published = models.BooleanField(
        _('Опубликован'),
        default=True,
        help_text=_('Показывать ли отзыв на сайте')
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв {self.id} к записи {self.appointment.id} ({self.rating}/5)"