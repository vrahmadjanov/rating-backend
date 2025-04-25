from rest_framework import viewsets
from django.utils import translation
from a_base.permissions import ReadOnlyOrAdmin
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
    
    def activate_language_from_header(self, request):
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        translation.activate(lang)