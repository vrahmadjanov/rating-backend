from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from a_base.models import Specialty
from doctors.models import Doctor

class DoctorSpecialtyInline(admin.TabularInline):
    """Inline для отображения связи ManyToMany с докторами"""
    model = Doctor.specialties.through
    extra = 1
    verbose_name = _("Врач")
    verbose_name_plural = _("Врачи с этой специализацией")
    raw_id_fields = ('doctor',)  # Для удобства при большом количестве врачей

@admin.register(Specialty)
class SpecialtyAdmin(TranslationAdmin):
    list_display = ('name', 'name_ru', 'name_tg', 'doctors_count')
    list_filter = ('name_ru', 'name_tg')
    search_fields = ('name_ru', 'name_tg')
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        (_("Русская версия"), {
            'fields': ('name_ru',),
            'classes': ('collapse',)
        }),
        (_("Таджикская версия"), {
            'fields': ('name_tg',),
            'classes': ('collapse',)
        }),
    )
    inlines = (DoctorSpecialtyInline,)

    def doctors_count(self, obj):
        return obj.doctor_set.count()
    doctors_count.short_description = _("Количество врачей")
    doctors_count.admin_order_field = 'doctor_count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(doctor_count=models.Count('doctor'))
        return queryset