from modeltranslation.translator import register, TranslationOptions
from django.contrib.auth.models import Group
from .models import (
    Region, District,
    Advantage, Subscription, Gender,
    Specialty, AcademicDegree, MedicalCategory, Service, ServicePlace, 
    Language, LanguageLevel, ExperienceLevel,
    SocialStatus, University
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

@register(MedicalCategory)
class MedicalCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(ServicePlace)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name',)
    
@register(ExperienceLevel)
class ExperienceLevelTranslationOptions(TranslationOptions):
    fields = ('level',)

# languages
@register(Language)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(LanguageLevel)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('level',)

# social statuses
@register(SocialStatus)
class SocialStatusTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# universities
@register(University)
class UniversityTranslationOptions(TranslationOptions):
    fields = ('name', 'city', 'country')