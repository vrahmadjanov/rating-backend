from django.utils import translation
from rest_framework import serializers
from a_base.models import Specialty
from django.conf import settings

class SpecialtySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    name_ru = serializers.CharField(write_only=True, required=False)
    name_tg = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'name_ru', 'name_tg']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def create(self, validated_data):
        name_ru = validated_data.pop('name_ru', None)
        name_tg = validated_data.pop('name_tg', None)
        
        specialty = Specialty.objects.create(
            name_ru=name_ru,
            name_tg=name_tg if name_tg else name_ru,  # Если таджикское не указано, используем русское
            **validated_data
        )
        return specialty
    
    def update(self, instance, validated_data):
        name_ru = validated_data.pop('name_ru', None)
        name_tg = validated_data.pop('name_tg', None)
        
        if name_ru is not None:
            instance.name_ru = name_ru
        if name_tg is not None:
            instance.name_tg = name_tg
        
        return super().update(instance, validated_data)
