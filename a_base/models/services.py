from django.db import models
from django.utils.translation import gettext_lazy as _

class ServicePlace(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Место предоставляемой услуги"))

    class Meta:
        verbose_name = _("Место предоставляемой услуги")
        verbose_name_plural = _("Места предоставляемых услуг")

    def __str__(self):
        return self.name

class Service(models.Model):
    service_place = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, verbose_name=_("Место предоставляемой услуги"))
    name = models.CharField(max_length=255, verbose_name=_("Название услуги"))
    description = models.TextField(blank=True, verbose_name=_("Описание услуги"))
    price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, verbose_name=_("Цена"))

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")

    def __str__(self):
        return self.name