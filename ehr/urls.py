from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitViewSet

router = DefaultRouter()
router.register(r'visits', VisitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
