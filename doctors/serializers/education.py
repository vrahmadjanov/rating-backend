from rest_framework import serializers
from ..models.education import Education
from doctors.serializers import DoctorSerializer

class EducationSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    
    class Meta:
        model = Education
        fields = ['id', 'doctor', 'institution_name', 'city', 'country', 'graduation_year']