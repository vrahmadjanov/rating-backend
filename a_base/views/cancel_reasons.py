from django.utils import translation
from rest_framework import viewsets
from a_base.models import CancelReason
from a_base.serializers import CancelReasonSerializer
from a_base.permissions import ReadOnlyOrAdmin

class CancelReasonViewSet(viewsets.ModelViewSet):
    queryset = CancelReason.objects.all()
    serializer_class = CancelReasonSerializer
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
