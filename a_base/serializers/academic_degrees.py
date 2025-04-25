from django.utils import translation
from rest_framework import serializers
from a_base.models import AcademicDegree
from django.conf import settings

class AcademicDegreeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = AcademicDegree
        fields = ['id', 'name']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))