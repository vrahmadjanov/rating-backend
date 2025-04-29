from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import Language, LanguageLevel

@admin.register(Language)
class LanguageAdmin(TranslationAdmin):
    list_display = ('name', 'name_ru', 'name_tg',)
    list_display_links = ('name_ru',)
    search_fields = ('name_ru', 'name_tg',)
    ordering = ('name',)

@admin.register(LanguageLevel)
class LanguageLevelAdmin(TranslationAdmin):
    list_display = ('level', 'level_ru', 'level_tg',)
    list_display_links = ('level_ru',)
    search_fields = ('level_ru', 'level_tg',)
    ordering = ('level',)