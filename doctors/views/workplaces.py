from rest_framework import viewsets

from doctors.models import Workplace
from doctors.serializers import WorkplaceSerializer

class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
