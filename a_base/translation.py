from modeltranslation.translator import register, TranslationOptions
from .models import (
    Region, District,
    Advantage, Subscription, Gender,
    Specialty, AcademicDegree
    )

# locations
@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)

# subscriptions
@register(Advantage)
class AdvantageTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Subscription)
class SubscriptionTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# gender
@register(Gender)
class GenderTranslationOptions(TranslationOptions):
    fields = ('name',)

# doctor profile information
@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(AcademicDegree)
class AcademicDegreeTranslationOptions(TranslationOptions):
    fields = ('name',)