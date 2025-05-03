from rest_framework import serializers
from doctors.models import Doctor
from a_base.models import Specialty, MedicalCategory, AcademicDegree, ExperienceLevel, Service
from a_base.serializers import (AcademicDegreeSerializer, SpecialtySerializer, MedicalCategorySerializer, 
                                ServiceSerializer, ExperienceLevelSerializer)
from core.serializers import CustomUserPublicSerializer, CustomUserPrivateSerializer

from django.utils import translation
from django.conf import settings

class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserPrivateSerializer()
    specialties = SpecialtySerializer(many=True, read_only=True)
    medical_category = MedicalCategorySerializer(read_only=True)
    academic_degree = AcademicDegreeSerializer(read_only=True)
    experience_level = ExperienceLevelSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    about = serializers.SerializerMethodField()
    philosophy = serializers.SerializerMethodField()
    titles_and_merits = serializers.SerializerMethodField()
    about_ru = serializers.CharField(write_only=True, required=True)
    about_tg = serializers.CharField(write_only=True, required=False)
    philosophy_ru = serializers.CharField(write_only=True, required=True)
    philosophy_tg = serializers.CharField(write_only=True, required=False)
    titles_and_merits_ru = serializers.CharField(write_only=True, required=True)
    titles_and_merits_tg = serializers.CharField(write_only=True, required=False)

    def get_about(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'about_{lang}', getattr(obj, f'about_{fallback_lang}', 'Нет перевода'))
    
    def get_philosophy(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'philosophy_{lang}', getattr(obj, f'philosophy_{fallback_lang}', 'Нет перевода'))

    def get_titles_and_merits(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'titles_and_merits_{lang}', getattr(obj, f'titles_and_merits_{fallback_lang}', 'Нет перевода'))

    specialties_ids = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(),
        source='specialties',
        required=False,
        many=True,
        write_only=True,
        allow_null=True
    )

    medical_category_id = serializers.PrimaryKeyRelatedField(
        queryset=MedicalCategory.objects.all(),
        source='medical_category',
        required=False,
        write_only=True,
        allow_null=True
    )

    academic_degree_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicDegree.objects.all(),
        source='academic_degree',
        required=False,
        write_only=True,
        allow_null=True
    )

    experience_level_id = serializers.PrimaryKeyRelatedField(
        queryset=ExperienceLevel.objects.all(),
        source='experience_level',
        required=False,
        write_only=True,
        allow_null=True
    )

    services_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='services',
        required=False,
        many=True,
        write_only=True,
        allow_null=True
    )

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 
            'specialties', 'medical_category', 'academic_degree', 'license_number',
            'experience_level', 'services', 'about', 'about_ru', 'about_tg', 'philosophy', 
            'philosophy_ru', 'philosophy_tg', 'titles_and_merits', 'titles_and_merits_ru', 
            'titles_and_merits_tg', 'work_phone_number', 'whatsapp', 'telegram',
            'created_at', 'updated_at',
            'specialties_ids', 'medical_category_id', 'academic_degree_id', 'experience_level_id', 'services_ids',
        ]


    def update(self, instance, validated_data):
        """Обновляет профиль врача"""
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user_serializer = CustomUserPrivateSerializer(
                instance.user, 
                data=user_data, 
                partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
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
        if 'about_ru' in validated_data:
            instance.about_ru = validated_data['about_ru']
        if 'about_tg' in validated_data:
            instance.about_tg = validated_data['about_tg']
        if 'philosophy_ru' in validated_data:
            instance.philosophy_ru = validated_data['philosophy_ru']
        if 'philosophy_tg' in validated_data:
            instance.philosophy_tg = validated_data['philosophy_tg']
        if 'titles_and_merits_ru' in validated_data:
            instance.titles_and_merits_ru = validated_data['titles_and_merits_ru']
        if 'titles_and_merits_tg' in validated_data:
            instance.titles_and_merits_tg = validated_data['titles_and_merits_tg']
        if 'work_phone_number' in validated_data:
            instance.work_phone_number = validated_data['work_phone_number']
        if 'whatsapp' in validated_data:
            instance.whatsapp = validated_data['whatsapp']
        if 'telegram' in validated_data:
            instance.telegram = validated_data['telegram']
        instance.save()
        return instance

class DoctorUpdateSerializer(DoctorSerializer):
    user = CustomUserPrivateSerializer(required=False)
    
    class Meta(DoctorSerializer.Meta):
        pass  # Наследуем все поля

    def update(self, instance, validated_data):
        # Обработка данных пользователя
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = CustomUserPrivateSerializer(
                instance.user, 
                data=user_data, 
                partial=True,
                context=self.context
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Обработка ManyToMany полей
        m2m_fields = {
            'specialties': instance.specialties,
            'services': instance.services
        }
        
        for field, manager in m2m_fields.items():
            if field in validated_data:
                manager.set(validated_data.pop(field))

        # Обновление остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance