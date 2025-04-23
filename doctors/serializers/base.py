# doctors/serializers/base.py
from rest_framework import serializers
from doctors.models import Workplace, MedicalInstitution

class BaseWorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = '__all__'

class BaseMedicalInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitution
        fields = '__all__'