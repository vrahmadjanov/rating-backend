from django.utils import translation
from rest_framework import viewsets, status
from rest_framework.response import Response
from a_base.models import MedicalCategory
from a_base.serializers import MedicalCategorySerializer
from a_base.permissions import ReadOnlyOrAdmin

class MedicalCategoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalCategory.objects.all()
    serializer_class = MedicalCategorySerializer
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

    def create(self, request, *args, **kwargs):
        """Создание новой медицинской категории с переводами"""
        self.activate_language_from_header(request)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Вручную сохраняем чтобы контролировать процесс
        try:
            category = MedicalCategory.objects.create(
                name_ru=request.data.get('name_ru', ''),
                name_tg=request.data.get('name_tg', '')
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.to_representation(category),
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Обновление медицинской категории с переводами"""
        self.activate_language_from_header(request)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Вручную обновляем поля перевода
        if 'name_ru' in request.data:
            instance.name_ru = request.data['name_ru']
        if 'name_tg' in request.data:
            instance.name_tg = request.data['name_tg']
        
        try:
            instance.save()
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(serializer.to_representation(instance))
