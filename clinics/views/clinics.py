from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import translation

from a_base.permissions import ReadOnlyOrAdmin
from clinics.models import Clinic
from clinics.serializers import ClinicSerializer
from clinics.filters import ClinicFilter

class ClinicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с клиниками.
    Поддерживает фильтрацию по региону, району и типу клиники.
    Доступ зависит от подписки пользователя.
    """
    serializer_class = ClinicSerializer
    permission_classes = [ReadOnlyOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClinicFilter

    def get_queryset(self):
        """
        Возвращает queryset клиник в зависимости от прав пользователя и его подписки.
        """
        queryset = Clinic.objects.select_related(
            'clinic_type', 
            'district', 
            'district__region'
        ).order_by('name')

        # Администраторы получают полный доступ
        if self.request.user.is_staff:
            return queryset

        # Проверка активной подписки
        if not hasattr(self.request.user, 'has_active_subscription') or \
           not self.request.user.has_active_subscription:
            return Clinic.objects.none()

        user_subscription = getattr(self.request.user, 'subscription', None)
        user_region = self.request.user.district.region

        # Определение доступных клиник по типу подписки
        subscription_access = {
            'Премиум': queryset,
            'Стандартная': queryset.filter(district__region=user_region) if user_region else Clinic.objects.none(),
            'Базовая': queryset.filter(district__region=user_region) if user_region else Clinic.objects.none(),
        }

        return subscription_access.get(user_subscription.name)

    def list(self, request, *args, **kwargs):
        """
        Список клиник с поддержкой языка из заголовка запроса.
        """
        self._activate_language_from_header(request)
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"detail": "Доступ к клиникам ограничен. Проверьте вашу подписку."},
                status=status.HTTP_403_FORBIDDEN
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Детальная информация о клинике с проверкой доступа.
        """
        self._activate_language_from_header(request)
        
        try:
            # Получаем queryset с учетом прав доступа
            queryset = self.get_queryset()
            
            # Получаем конкретную клинику или возвращаем 404
            instance = queryset.get(id=kwargs['pk'])
            
            # Сериализуем данные
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            
        except Clinic.DoesNotExist:
            # Если клиника не найдена в доступном queryset
            return Response(
                {"detail": "Клиника не найдена или у вас нет доступа"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Обработка других ошибок
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _activate_language_from_header(self, request):
        """
        Активирует язык из заголовка запроса.
        По умолчанию: русский ('ru').
        """
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        translation.activate(lang)