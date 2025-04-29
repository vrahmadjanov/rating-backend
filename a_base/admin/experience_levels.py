from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import ExperienceLevel


@admin.register(ExperienceLevel)
class ExperienceLevelAdmin(TranslationAdmin):
    list_display = ('level', 'level_ru', 'level_tg',)
    list_display_links = ('level_ru',)
    search_fields = ('level_ru', 'level_tg',)
    ordering = ('level',)