# urls.py
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SendEmail
from .views import SendSMSView, SendPushView, SaveDeviceTokenView

router = DefaultRouter()
router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/save-device-token/', SaveDeviceTokenView.as_view(), name='save-device-token'),

    path('send-email/', SendEmail.as_view(), name='send-email'),
    path('send-sms/', SendSMSView.as_view(), name='send-sms'),
    path('send-push/', SendPushView.as_view(), name='send-push'),
]
