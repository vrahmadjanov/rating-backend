from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для получения списка доступных подписок.
    Возвращает данные в формате:
    {
        "id": 1,
        "name": "Базовая",
        "description": "...",
        "price": 0,
        "duration_days": 30,
        "advantages": ["...", "..."]
    }
    """
    queryset = Subscription.objects.filter(is_active=True).prefetch_related('advantages')
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации

    def get_queryset(self):
        """Возвращаем подписки, отсортированные по цене"""
        return super().get_queryset().order_by('price')