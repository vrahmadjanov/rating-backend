from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название услуги")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name