from rest_framework import serializers
from doctors.models import Doctor
from a_base.models import Specialty, MedicalCategory, AcademicDegree, ExperienceLevel, Service
from a_base.serializers import (AcademicDegreeSerializer, SpecialtySerializer, MedicalCategorySerializer, 
                                ServiceSerializer, ExperienceLevelSerializer)
from core.serializers import CustomUserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    specialties = SpecialtySerializer(many=True, read_only=True)
    medical_category = MedicalCategorySerializer(read_only=True)
    academic_degree = AcademicDegreeSerializer(read_only=True)
    experience_level = ExperienceLevelSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    specialties_ids = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(),
        source='specialties',
        allow_null=True,
        many=True,
        write_only=True
    )

    medical_category_id = serializers.PrimaryKeyRelatedField(
        queryset=MedicalCategory.objects.all(),
        source='medical_category',
        allow_null=True,
        write_only=True
    )

    academic_degree_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicDegree.objects.all(),
        source='academic_degree',
        allow_null=True,
        write_only=True
    )

    experience_level_id = serializers.PrimaryKeyRelatedField(
        queryset=ExperienceLevel.objects.all(),
        source='experience_level',
        allow_null=True,
        write_only=True
    )

    services_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='services',
        allow_null=True,
        many=True,
        write_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 
            'specialties', 'medical_category', 'academic_degree', 'license_number',
            'experience_level', 'services', 'about', 'philosophy', 'titles_and_merits', 
            'work_phone_number', 'whatsapp', 'telegram',
            'created_at', 'updated_at',
            'specialties_ids', 'medical_category_id', 'academic_degree_id', 'experience_level_id', 'services_ids',
        ]

    def update(self, instance, validated_data):
        """Обновляет профиль врача"""
        
        if 'specialties' in validated_data:
            instance.specialties.set(validated_data['specialties'])
        if 'medical_category' in validated_data:
            instance.medical_category = validated_data['medical_category']
        if 'academic_degree' in validated_data:
            instance.academic_degree = validated_data['academic_degree']
        if 'license_number' in validated_data:
            instance.license_number = validated_data['license_number']
        if 'experience_level' in validated_data:
            instance.experience_level = validated_data['experience_level']
        if 'services' in validated_data:
            instance.services.set(validated_data['services'])
        if 'about' in validated_data:
            instance.about = validated_data['about']
        if 'philosophy' in validated_data:
            instance.philosophy = validated_data['philosophy']
        if 'titles_and_merits' in validated_data:
            instance.titles_and_merits = validated_data['titles_and_merits']
        if 'work_phone_number' in validated_data:
            instance.work_phone_number = validated_data['work_phone_number']
        if 'whatsapp' in validated_data:
            instance.whatsapp = validated_data['whatsapp']
        if 'telegram' in validated_data:
            instance.telegram = validated_data['telegram']
        instance.save()
        return instance
    
    def create(self, validated_data):
        """Создает профиль врача"""
        user_data = validated_data.pop('user')
        specialties = validated_data.pop('specialties', [])
        services = validated_data.pop('services', [])
        
        # Создаем пользователя
        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            raise serializers.ValidationError(user_serializer.errors)
        
        # Создаем врача
        doctor = Doctor.objects.create(user=user, **validated_data)
        
        # Добавляем many-to-many отношения
        doctor.specialties.set(specialties)
        doctor.services.set(services)
        
        return doctor