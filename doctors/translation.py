from modeltranslation.translator import register, TranslationOptions
from .models import Doctor

@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('about', 'philosophy', 'titles_and_merits')
