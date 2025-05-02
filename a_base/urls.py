from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DistrictViewSet, RegionViewSet, SubscriptionViewSet, GroupViewSet,
                    AcademicDegreeViewSet, SpecialtyViewSet, MedicalCategoryViewSet, ServiceViewSet,
                    LanguageViewSet, LanguageLevelViewSet, GenderViewSet, ExperienceLevelViewSet,
                    SocialStatusViewSet)

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'groups', GroupViewSet, basename='group')

router.register(r'academic_degrees', AcademicDegreeViewSet, basename='academic_degree')
router.register(r'medical_categories', MedicalCategoryViewSet, basename='medical_category')
router.register(r'specialties', SpecialtyViewSet, basename='specialty')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'genders', GenderViewSet, basename='gender')
router.register(r'experience_levels', ExperienceLevelViewSet, basename='experience_level')

router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'language_levels', LanguageLevelViewSet, basename='language_level')

router.register(r'social_statuses', SocialStatusViewSet, basename='social_status')


urlpatterns = [
    path('', include(router.urls)),
]
