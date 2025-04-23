from django.db import models

class MedicalCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название медицинской категории")

    class Meta:
        verbose_name = "Медицинская категория"
        verbose_name_plural = "Медицинские категории"

    def __str__(self):
        return self.name