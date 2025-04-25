from rest_framework import serializers
from ..models.doctors import Doctor, Specialty, MedicalCategory, Service
from a_base.serializers import AcademicDegreeSerializer
from .language import UserLanguageSerializer
from core.serializers import CustomUserSerializer, CustomUserShortSerializer
from .workplace import WorkplaceSerializer, WorkplaceShortSerializer
from .education import EducationSerializer
from .schedule import ScheduleSerializer

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name']

class MedicalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCategory
        fields = ['name']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']

class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    specialty = SpecialtySerializer()
    medical_category = MedicalCategorySerializer()
    services = ServiceSerializer(many=True)
    workplaces = WorkplaceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    user_languages = UserLanguageSerializer(many=True)
    academic_degree = AcademicDegreeSerializer()

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'specialty', 'medical_category', 'academic_degree', 
            'philosophy', 'services', 'license_number', 'is_verified', 'verification_date', 
            'verified_by', 'titles_and_merits', 'workplaces', 'educations', 'schedules', 
            'experience_years', 'user_languages'
        ]


class DoctorCardSerializer(serializers.ModelSerializer):
    user = CustomUserShortSerializer(read_only=True)
    workplaces = WorkplaceShortSerializer(many=True, read_only=True)
    medical_category = MedicalCategorySerializer()
    academic_degree = AcademicDegreeSerializer()
    services = ServiceSerializer(many=True)
    user_languages = UserLanguageSerializer(many=True)
    specialty = SpecialtySerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            'user', 'experience_years', 'academic_degree', 'specialty',
            'medical_category', 'services', 'user_languages', 'workplaces'
        ]

class DoctorShortSerializer(serializers.ModelSerializer):
    user = CustomUserShortSerializer(read_only=True)
    workplaces = WorkplaceShortSerializer(many=True, read_only=True)
    specialty = SpecialtySerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'workplaces', 'specialty'
        ]