from django.db import models
from django.utils.translation import gettext_lazy as _
from a_base.models import Language, LanguageLevel

class DoctorLanguage(models.Model):
    """
    Модель для хранения информации о языках, которыми владеет доктор, и их уровне владения.
    """
    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.CASCADE,
        related_name="languages",
        verbose_name=_("Доктор")
    )
    
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name=_("Язык")
    )
    
    level = models.ForeignKey(
        LanguageLevel,
        on_delete=models.CASCADE,
        verbose_name=_("Уровень владения")
    )

    class Meta:
        verbose_name = _("Язык доктора")
        verbose_name_plural = _("Языки доктора")
        unique_together = ('doctor', 'language')

    def __str__(self):
        return f"{self.doctor.user.get_full_name} {self.language} ({self.level})"
