from django.db import models

class Language(models.Model):
    """
    Модель для хранения информации о языках.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Язык",
        help_text="Название языка",
        unique=True  # Уникальность названия языка
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

class LanguageLevel(models.Model):
    """
    Модель для хранения информации об уровнях владения языком.
    """
    level = models.CharField(
        max_length=100,
        verbose_name="Уровень владения",
        help_text="Уровень владения языком",
        unique=True  # Уникальность уровня
    )

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = "Уровень владения языком"
        verbose_name_plural = "Уровни владения языками"

class UserLanguage(models.Model):
    """
    Модель для хранения информации о языках, которыми владеет доктор, и их уровне владения.
    """
    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.CASCADE,
        related_name="user_languages",
        verbose_name="Доктор"
    )
    
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name="Язык"
    )
    
    level = models.ForeignKey(
        LanguageLevel,
        on_delete=models.CASCADE,
        verbose_name="Уровень владения"
    )

    class Meta:
        verbose_name = "Язык доктора"
        verbose_name_plural = "Языки доктора"
        unique_together = ('doctor', 'language')  # Уникальность по доктору и языку

    def __str__(self):
        return f"{self.doctor} - {self.language} ({self.level})"
