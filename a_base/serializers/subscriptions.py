from rest_framework import serializers
from django.utils import translation
from django.conf import settings
from a_base.models import Subscription, Advantage

class AdvantageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    class Meta:
        model = Advantage
        fields = ['id', 'name', 'description']

    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def get_description(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'description_{lang}', getattr(obj, f'description_{fallback_lang}', 'Нет перевода'))


class SubscriptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    advantages = AdvantageSerializer(many=True)

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'description', 'price', 'duration_days', 'advantages']

    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def get_description(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'description_{lang}', getattr(obj, f'description_{fallback_lang}', 'Нет перевода'))