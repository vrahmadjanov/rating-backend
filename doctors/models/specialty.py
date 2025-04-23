from django.db import models

class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название специальности")

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

    def __str__(self):
        return self.name