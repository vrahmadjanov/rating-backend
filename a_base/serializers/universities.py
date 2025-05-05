from django.utils import translation
from rest_framework import serializers
from a_base.models import University
from django.conf import settings

class UniversitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    name_ru = serializers.CharField(write_only=True, required=True)
    name_tg = serializers.CharField(write_only=True, required=False)
    city_ru = serializers.CharField(write_only=True, required=True)
    city_tg = serializers.CharField(write_only=True, required=True)
    country_ru = serializers.CharField(write_only=True, required=True)
    country_tg = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'name_ru', 'name_tg',
                  'city', 'city_ru', 'city_tg',
                  'country', 'country_ru', 'country_tg']

    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def get_city(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'city_{lang}', getattr(obj, f'city_{fallback_lang}', 'Нет перевода'))
    
    def get_country(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'country_{lang}', getattr(obj, f'country_{fallback_lang}', 'Нет перевода'))
    
    
    def create(self, validated_data):
        """Создает вуз с переводами"""

        return University.objects.create(
            name_ru=validated_data['name_ru'],
            name_tg=validated_data.get('name_tg', validated_data['name_ru']),
            city_ru=validated_data['city_ru'],
            city_tg=validated_data.get('city_tg', validated_data['city_ru']),
            country_ru=validated_data['country_ru'],
            country_tg=validated_data.get('country_tg', validated_data['country_ru']),
        )
    
    def update(self, instance, validated_data):
        """Обновляет вуз с переводами"""

        instance.name_ru = validated_data.get('name_ru', instance.name_ru)
        instance.name_tg = validated_data.get('name_tg', instance.name_tg)
        instance.city_ru = validated_data.get('city_ru', instance.city_ru)
        instance.city_tg = validated_data.get('city_tg', instance.city_tg)
        instance.country_ru = validated_data.get('country_ru', instance.country_ru)
        instance.country_tg = validated_data.get('country_tg', instance.country_tg)

        instance.save()
        return instance