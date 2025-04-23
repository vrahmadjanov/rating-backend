from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, SocialStatusViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'social-statuses', SocialStatusViewSet, basename='social-status')

urlpatterns = [
    path('', include(router.urls)),
]
