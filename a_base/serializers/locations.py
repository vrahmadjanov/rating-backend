from rest_framework import serializers
from a_base.models import City, Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = City
        fields = '__all__'