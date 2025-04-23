from modeltranslation.translator import register, TranslationOptions
from .models import Region, City

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)