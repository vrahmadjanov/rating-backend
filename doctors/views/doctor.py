# doctors/views/doctor.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny

from doctors.models import Doctor, Education
from doctors.serializers import EducationSerializer, DoctorSerializer
from doctors.permissions import IsAdminOrReadOnly
from doctors.filters import DoctorFilter

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Для администраторов возвращаем все записи
        if self.request.user.is_staff:
            return queryset
            
        # Проверяем активную подписку
        if not self.request.user.has_active_subscription:
            return Doctor.objects.none()
            
        # Получаем подписку пользователя
        user_subscription = self.request.user.subscription
        
        # Если подписка не найдена, не показываем врачей
        if not user_subscription:
            return Doctor.objects.none()
            
        # Получаем регион пользователя
        user_region = self.request.user.city.region if self.request.user.city else None
        
        # Определяем доступные регионы в зависимости от подписки
        if user_subscription.name == 'Премиум':
            # Для премиум подписки доступны все врачи
            return queryset
        
        elif user_subscription.name == 'Стандартная':
            # Для базовой подписки только врачи из своего региона
            if user_region:
                return queryset.filter(user__city__region=user_region)

        elif user_subscription.name == 'Базовая':
            # Для базовой подписки только врачи из своего региона
            if user_region:
                return queryset.filter(user__city__region=user_region)
            return Doctor.objects.none()
        else:
            # Для других типов подписок (если будут добавлены)
            return Doctor.objects.none()

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer