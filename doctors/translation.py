from modeltranslation.translator import register, TranslationOptions
from .models import Doctor, Workplace

@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('about', 'philosophy', 'titles_and_merits')

@register(Workplace)
class WorkplaceTranslationOptions(TranslationOptions):
    fields = ('position',)  
