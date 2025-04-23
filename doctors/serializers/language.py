from rest_framework import serializers
from ..models.language import Language, LanguageLevel, UserLanguage

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']

class LanguageLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageLevel
        fields = ['level']

class UserLanguageSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    level = LanguageLevelSerializer()

    class Meta:
        model = UserLanguage
        fields = ['language', 'level']