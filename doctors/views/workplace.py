from rest_framework import viewsets

from doctors.models import Workplace, Schedule
from doctors.serializers import WorkplaceSerializer, ScheduleSerializer

class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer