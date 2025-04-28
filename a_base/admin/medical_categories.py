from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import MedicalCategory

@admin.register(MedicalCategory)
class MedicalCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'name_ru', 'name_tg',)
    list_display_links = ('name',)
    search_fields = ('name_ru', 'name_tg',)
    ordering = ('name',)