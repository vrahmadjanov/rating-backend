from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Region, City

@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    pass

@admin.register(City)
class CityAdmin(TranslationAdmin):
    pass
