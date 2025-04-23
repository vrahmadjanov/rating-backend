from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from a_base.models import City, Region
from a_base.serializers import CitySerializer, RegionSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]
