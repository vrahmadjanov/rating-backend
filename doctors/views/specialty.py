from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from doctors.models import Specialty
from doctors.serializers import SpecialtySerializers

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]