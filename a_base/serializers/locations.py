from django.utils import translation
from rest_framework import serializers
from a_base.models import Region, District
from django.conf import settings

class RegionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Region
        fields = ['id','code', 'name']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))

class DistrictSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    region = RegionSerializer(read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'code', 'name', 'region']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))