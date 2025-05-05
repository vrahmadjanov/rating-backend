from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import University

@admin.register(University)
class UniversityAdmin(TranslationAdmin):
    list_display = ('name_ru', 'name_tg', 'city_ru', 'country_ru')
    list_display_links = ('name_ru',)
    search_fields = ('name_ru', 'city_ru', 'country_ru')
    ordering = ('name_ru',)