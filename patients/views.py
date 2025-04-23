from rest_framework import viewsets
from .models import Patient, SocialStatus
from .serializers import PatientSerializer, SocialStatusSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SocialStatusViewSet(viewsets.ModelViewSet):
    queryset = SocialStatus.objects.all()
    serializer_class = SocialStatusSerializer
