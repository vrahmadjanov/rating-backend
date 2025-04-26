from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, MedicalInstitutionViewSet, WorkplaceViewSet, ScheduleViewSet, EducationViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'medical-institutions', MedicalInstitutionViewSet, basename='medical-institution')
router.register(r'workplaces', WorkplaceViewSet, basename='workplace')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'educations', EducationViewSet, basename='education')

urlpatterns = [
    path('', include(router.urls)),
]
