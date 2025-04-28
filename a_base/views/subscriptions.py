from rest_framework import viewsets, status
from django.utils import translation
from a_base.permissions import ReadOnlyOrAdmin
from rest_framework.response import Response
from rest_framework.decorators import action
from a_base.models import Subscription
from a_base.serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для получения списка доступных подписок.
    """
    queryset = Subscription.objects.filter(is_active=True)
    serializer_class = SubscriptionSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def list(self, request, *args, **kwargs):
        # Принудительно активируем язык из заголовка
        self.activate_language_from_header(request)
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.activate_language_from_header(request)
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """Активация подписки для текущего пользователя"""
        subscription = self.get_object()
        request.user.subscription = subscription
        request.user.activate_subscription()
        request.user.save()
        return Response({'status': 'subscription activated'}, status=status.HTTP_201_CREATED)
    
    def activate_language_from_header(self, request):
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        translation.activate(lang)