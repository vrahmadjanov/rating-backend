from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appointment

admin.site.register(Appointment)