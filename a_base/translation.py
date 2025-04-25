from modeltranslation.translator import register, TranslationOptions
from .models import (
    Region, District,
    Advantage, Subscription,
    AcademicDegree, Gender
    )

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(AcademicDegree)
class AcademicDegreeTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Advantage)
class AdvantageTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Subscription)
class SubscriptionTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Gender)
class GenderTranslationOptions(TranslationOptions):
    fields = ('name',)