from django.utils import translation
from rest_framework import serializers
from a_base.models import SocialStatus
from django.conf import settings

class SocialStatusSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialStatus
        fields = ['id', 'name', 'description']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def get_description(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'description_{lang}', getattr(obj, f'description_{fallback_lang}', 'Нет перевода'))