from rest_framework import serializers
from .models import City, Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            'name' 
        ]

class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = City
        fields = [
            'id', 'region', 'name'
        ]