from modeltranslation.translator import register, TranslationOptions
from .models import ClinicType, Clinic

# locations
@register(ClinicType)
class ClinicTypeTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Clinic)
class ClinicTranslationOptions(TranslationOptions):
    fields = ('name', 'address',)

