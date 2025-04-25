from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DistrictViewSet, RegionViewSet, AcademicDegreeViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'academic_degrees', AcademicDegreeViewSet, basename='academic_degree')


urlpatterns = [
    path('', include(router.urls)),
]
