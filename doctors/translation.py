from modeltranslation.translator import register, TranslationOptions
from .models import Doctor, Education

@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('about', 'philosophy', 'titles_and_merits')

@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = ('institution_name', 'city', 'country')  
