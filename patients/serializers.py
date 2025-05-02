from rest_framework import serializers
from .models import Patient
from core.serializers import CustomUserSerializer
from a_base.serializers import SocialStatusSerializer


class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    social_status = SocialStatusSerializer()

    class Meta:
        model = Patient
        fields = [
            'id','user', 'passport', 'registration_address',
            'actual_address', 'sin', 'eng', 'social_status',
        ]