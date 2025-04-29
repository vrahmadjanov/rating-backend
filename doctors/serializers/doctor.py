from rest_framework import serializers
from ..models.doctors import Doctor
from a_base.serializers import AcademicDegreeSerializer, SpecialtySerializer, MedicalCategorySerializer, ServiceSerializer
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

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'specialties', 'medical_category', 'academic_degree', 
            'philosophy', 'services', 'license_number', 'is_verified', 'verification_date', 
            'verified_by', 'titles_and_merits', 'educations', 'experience_years', 'languages'
        ]