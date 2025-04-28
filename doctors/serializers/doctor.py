from rest_framework import serializers
from ..models.doctors import Doctor, Service
from a_base.serializers import AcademicDegreeSerializer, SpecialtySerializer, MedicalCategorySerializer
from .language import UserLanguageSerializer
from core.serializers import CustomUserSerializer
from .education import EducationSerializer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']

class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    specialties = SpecialtySerializer(many=True)
    medical_category = MedicalCategorySerializer()
    services = ServiceSerializer(many=True)
    educations = EducationSerializer(many=True, read_only=True)
    user_languages = UserLanguageSerializer(many=True)
    academic_degree = AcademicDegreeSerializer()

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'specialties', 'medical_category', 'academic_degree', 
            'philosophy', 'services', 'license_number', 'is_verified', 'verification_date', 
            'verified_by', 'titles_and_merits', 'educations', 'experience_years', 'user_languages'
        ]