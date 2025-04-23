from rest_framework import viewsets
from .serializers import AppointmentSerializer, AppointmentShortSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .permissions import IsAdminOrPatientOwner
from patients.models import Patient

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentShortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPatientOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient']

    def get_queryset(self):
        """
        Админы видят все записи, пациенты - только свои
        """
        user = self.request.user
        patient = Patient.objects.get(user=user)
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(patient=patient)