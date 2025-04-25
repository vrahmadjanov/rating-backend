from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    
    path('api/', include("core.urls")),
    path('api/', include("doctors.urls")),
    path('api/', include("patients.urls")),
    path('api/', include("ehr.urls")),
    path('api/', include("chat.urls")),
    path('api/', include("appointments.urls")),
    path('api/', include("a_base.urls")),

    path('notifications/', include("notifications.urls")),
]
