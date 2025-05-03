# doctors/serializers/workplace.py
from rest_framework import serializers
from doctors.serializers import DoctorSerializer
from clinics.serializers import ClinicSerializer
from doctors.models import Workplace


class WorkplaceSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = Workplace
        fields = '__all__'
