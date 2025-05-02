from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from doctors.models import Education
from doctors.serializers import EducationSerializer
from doctors.permissions import IsAdminOrReadOnly

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer