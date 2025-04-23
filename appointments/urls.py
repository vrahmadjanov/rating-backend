# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

# Создаем экземпляр роутера
router = DefaultRouter()

# Регистрируем наш ViewSet
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # Подключаем URL-адреса, которые создал роутер
    path('', include(router.urls)),
]