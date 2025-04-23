from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet, RegionViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'regions', RegionViewSet, basename='region')


urlpatterns = [
    path('', include(router.urls)),
]
