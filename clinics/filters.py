# doctors/filters.py
import django_filters
from .models import Clinic

class ClinicFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains') # Поиск по подстроке
    district = django_filters.CharFilter(field_name='district__name', lookup_expr='icontains')
    region = django_filters.CharFilter(field_name='city__region__name', lookup_expr='icontains') 
    clinic_type = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Clinic
        fields = ['name', 'district', 'region', 'clinic_type']
