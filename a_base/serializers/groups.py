from django.utils import translation
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.conf import settings

class GroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
