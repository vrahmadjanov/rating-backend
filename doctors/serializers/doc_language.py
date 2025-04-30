from rest_framework import serializers
from doctors.models import DoctorLanguage
from a_base.models import Language, LanguageLevel
from doctors.serializers import DoctorSerializer
from a_base.serializers import LanguageLevelSerializer, LanguageSerializer

class DoctorLanguageSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    language = LanguageSerializer(read_only=True)
    level = LanguageLevelSerializer(read_only=True)

    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        source='language',
        write_only=True
    )

    level_id = serializers.PrimaryKeyRelatedField(
        queryset=LanguageLevel.objects.all(),
        source='level',
        write_only=True
    )

    class Meta:
        model = DoctorLanguage
        fields = ['id', 'doctor', 'language', 'language_id', 'level', 'level_id',]