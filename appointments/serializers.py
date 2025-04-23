from rest_framework import serializers
from .models import Appointment, Review
from patients.serializers import PatientSerializer, PatientShortSerializer
from doctors.serializers import DoctorSerializer, DoctorShortSerializer, DoctorCardSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'start_time', 'end_time', 'status',
                  'cancellation_reason', 'cancellation_notes', 'cancelled_at', 'phone_number',
                  'is_another_patient', 'another_patient_name', 'another_patient_age', 
                  'another_patient_gender', 'problem_description']

class AppointmentShortSerializer(serializers.ModelSerializer):
    patient = PatientShortSerializer()
    doctor = DoctorShortSerializer()
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'start_time', 'end_time', 'status',
                  'is_another_patient', 'another_patient_name', 'another_patient_age', 
                  'another_patient_gender', 'problem_description']
