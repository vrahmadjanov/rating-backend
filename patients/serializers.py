from rest_framework import serializers
from .models import Patient, SocialStatus
from core.serializers import CustomUserSerializer, CustomUserShortSerializer

class SocialStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialStatus
        fields = ['name']

class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    social_status = SocialStatusSerializer()

    class Meta:
        model = Patient
        fields = [
            'id','user', 'passport', 'registration_address',
            'actual_address', 'sin', 'eng', 'social_status',
        ]

class PatientShortSerializer(serializers.ModelSerializer):
    user = CustomUserShortSerializer()
    social_status = SocialStatusSerializer()

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'actual_address', 'social_status',
        ]