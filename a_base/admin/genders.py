from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import Gender

@admin.register(Gender)
class GenderAdmin(TranslationAdmin):
    list_display = ('name', 'name_ru', 'name_tg',)
    list_display_links = ('name_ru',)
    search_fields = ('name_ru', 'name_tg',)
    ordering = ('name',)

