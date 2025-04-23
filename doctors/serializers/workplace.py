# doctors/serializers/workplace.py
from rest_framework import serializers
from doctors.models import Workplace
from .base import BaseWorkplaceSerializer

def get_medical_institution_serializer():
    from .medical_institution import MedicalInstitutionSerializer
    return MedicalInstitutionSerializer

def get_medical_institution_short_serializer():
    from .medical_institution import MedicalInstitutionShortSerializer
    return MedicalInstitutionShortSerializer

def get_schedule_serializer():
    from .schedule import ScheduleSerializer
    return ScheduleSerializer

class WorkplaceSerializer(BaseWorkplaceSerializer):
    medical_institution = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

    def get_medical_institution(self, obj):
        serializer_class = get_medical_institution_serializer()
        return serializer_class(obj.medical_institution, read_only=True).data

    def get_schedule(self, obj):
        serializer_class = get_schedule_serializer()
        return serializer_class(obj.schedule, read_only=True).data

    class Meta(BaseWorkplaceSerializer.Meta):
        fields = ['medical_institution', 'position', 
                 'start_date', 'end_date', 'schedule']

class WorkplaceShortSerializer(BaseWorkplaceSerializer):
    medical_institution = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

    def get_medical_institution(self, obj):
        serializer_class = get_medical_institution_short_serializer()
        return serializer_class(obj.medical_institution, read_only=True).data
    
    def get_schedule(self, obj):
        serializer_class = get_schedule_serializer()
        return serializer_class(obj.schedule, read_only=True).data

    class Meta(BaseWorkplaceSerializer.Meta):
        fields = ['medical_institution', 'schedule']