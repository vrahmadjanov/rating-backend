from rest_framework import serializers
from ..models.doc_languages import DoctorLanguage
from a_base.serializers import LanguageLevelSerializer, LanguageSerializer

class DoctorLanguageSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    level = LanguageLevelSerializer()

    class Meta:
        model = DoctorLanguage
        fields = ['language', 'level']