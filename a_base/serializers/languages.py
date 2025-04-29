from django.utils import translation
from rest_framework import serializers
from a_base.models import Language, LanguageLevel
from django.conf import settings

class LanguageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Language
        fields = ['id', 'name']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
class LanguageLevelSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    
    class Meta:
        model = LanguageLevel
        fields = ['id', 'level']
    
    def get_level(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'level_{lang}', getattr(obj, f'level_{fallback_lang}', 'Нет перевода'))