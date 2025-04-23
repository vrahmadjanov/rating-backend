from django.db import models

class AcademicDegree(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название учёной степени")

    class Meta:
        verbose_name = "Научная степень"
        verbose_name_plural = "Научные степени"

    def __str__(self):
        return self.name