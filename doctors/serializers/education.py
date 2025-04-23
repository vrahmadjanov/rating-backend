from rest_framework import serializers
from ..models.education import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution_name', 'city', 'country', 'graduation_year']