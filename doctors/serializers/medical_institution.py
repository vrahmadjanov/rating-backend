# doctors/serializers/medical_institution.py
from rest_framework import serializers
from doctors.models.medical_institution import MedicalInstitution
from a_base.serializers import CitySerializer, RegionSerializer
from .base import BaseMedicalInstitutionSerializer

class MedicalInstitutionSerializer(BaseMedicalInstitutionSerializer):
    city = CitySerializer()
    region = RegionSerializer()
    
    class Meta(BaseMedicalInstitutionSerializer.Meta):
        fields = [
            'id', 'name', 'institution_type', 'country', 'region', 
            'city', 'address', 'phone_number', 'email', 'website'
        ]

class MedicalInstitutionShortSerializer(BaseMedicalInstitutionSerializer):
    city = CitySerializer()
    
    class Meta(BaseMedicalInstitutionSerializer.Meta):
        fields = ['id', 'name', 'city', 'address']