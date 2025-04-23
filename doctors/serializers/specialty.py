from rest_framework import serializers
from ..models import Specialty

class SpecialtySerializers(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name']