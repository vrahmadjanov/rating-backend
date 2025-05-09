from rest_framework import viewsets
from patients.models import Patient
from patients.serializers import PatientPublicSerializer, PatientPrivateSerializer
from a_base.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Определяем какой сериализатор использовать
        if self.action in ['retrieve', 'update', 'partial_update']:
            obj = self.get_object()
            if obj.user == self.request.user or self.request.user.is_staff:
                return PatientPrivateSerializer
        return PatientPublicSerializer

    def get_queryset(self):
        # Для не-админов показываем только их собственный профиль
        if not self.request.user.is_staff:
            return Patient.objects.filter(user=self.request.user)
        return super().get_queryset()
    
    def get_object(self):
        obj = super().get_object()
        # Дополнительная проверка для детального просмотра
        if not (self.request.user.is_staff or 
                self.request.user.is_superuser or 
                obj.user == self.request.user):
            self.permission_denied(self.request)
        return obj
