from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DistrictViewSet, RegionViewSet, SubscriptionViewSet, 
                    AcademicDegreeViewSet, SpecialtyViewSet)

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

router.register(r'academic_degrees', AcademicDegreeViewSet, basename='academic_degree')
router.register(r'specialties', SpecialtyViewSet, basename='specialty')


urlpatterns = [
    path('', include(router.urls)),
]
