from modeltranslation.translator import register, TranslationOptions
from .models import Region, District

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)