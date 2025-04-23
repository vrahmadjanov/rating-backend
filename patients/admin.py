from django.contrib import admin
from .models import Patient, SocialStatus

admin.site.register(Patient)
admin.site.register(SocialStatus)