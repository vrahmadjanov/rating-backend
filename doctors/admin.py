from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (Doctor,
                     Workplace, Education, DoctorLanguage,
                     Schedule)

admin.site.register(Doctor)
admin.site.register(DoctorLanguage)
admin.site.register(Workplace)
admin.site.register(Education)
admin.site.register(Schedule)
