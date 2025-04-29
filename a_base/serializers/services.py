from django.utils import translation
from rest_framework import serializers
from a_base.models import Service, ServicePlace
from django.conf import settings

class ServicePlaceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    name_ru = serializers.CharField(write_only=True, required=True)
    name_tg = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ServicePlace
        fields = ['id', 'name', 'name_ru', 'name_tg']

    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    

class ServiceSerializer(serializers.ModelSerializer):
    service_place = ServicePlaceSerializer(read_only=True)
    service_place_id = serializers.PrimaryKeyRelatedField(
        queryset=ServicePlace.objects.all(),
        source='service_place',
        write_only=True
    )

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    name_ru = serializers.CharField(write_only=True, required=True)
    name_tg = serializers.CharField(write_only=True, required=False)
    description_ru = serializers.CharField(write_only=True, required=True)
    description_tg = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'name_ru', 'name_tg', 'description_ru', 'description_tg', 
                  'service_place', 'service_place_id', 'price']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def get_description(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'description_{lang}', getattr(obj, f'description_{fallback_lang}', 'Нет перевода'))
    
    def create(self, validated_data):
        """Создает услугу с переводами"""
        service_place = validated_data.pop('service_place')

        return Service.objects.create(
            service_place=service_place,
            name_ru=validated_data['name_ru'],
            name_tg=validated_data.get('name_tg', validated_data['name_ru']),
            description_ru=validated_data['description_ru'],
            description_tg=validated_data.get('description_tg', validated_data['description_ru']),
            price=validated_data['price']
        )
    
    def update(self, instance, validated_data):
        """Обновляет переводы услуги"""
        
        if 'service_place' in validated_data:
            instance.service_place = validated_data['service_place']

        instance.name_ru = validated_data.get('name_ru', instance.name_ru)
        instance.name_tg = validated_data.get('name_tg', instance.name_tg)
        instance.description_ru = validated_data.get('description_ru', instance.description_ru)
        instance.description_tg = validated_data.get('description_tg', instance.description_tg)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance