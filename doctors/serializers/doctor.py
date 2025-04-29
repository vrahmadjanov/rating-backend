from rest_framework import serializers
from ..models.doctors import Doctor
from a_base.serializers import (AcademicDegreeSerializer, SpecialtySerializer, MedicalCategorySerializer, 
                                ServiceSerializer, ExperienceLevelSerializer)
from .doc_language import DoctorLanguageSerializer
from core.serializers import CustomUserSerializer
from .education import EducationSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    specialties = SpecialtySerializer(many=True)
    medical_category = MedicalCategorySerializer()
    services = ServiceSerializer(many=True)
    educations = EducationSerializer(many=True, read_only=True)
    languages = DoctorLanguageSerializer(many=True)
    academic_degree = AcademicDegreeSerializer()
    experience_level = ExperienceLevelSerializer()

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'specialties', 'medical_category', 'academic_degree', 'about',
            'philosophy', 'services', 'license_number','titles_and_merits', 'educations', 
            'experience_level', 'languages', 'created_at', 'work_phone_number', 'telegram',
            'whatsapp',
        ]