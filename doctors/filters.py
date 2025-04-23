# doctors/filters.py
import django_filters
from dateutil.relativedelta import relativedelta
import datetime
from .models.medical_institution import MedicalInstitution
from .models.doctors import Doctor

class MedicalInstitutionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # Поиск по подстроке
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')  # Фильтрация по городу
    region = django_filters.CharFilter(field_name='region__name', lookup_expr='icontains')  # Фильтрация по региону
    institution_type = django_filters.CharFilter(lookup_expr='exact')  # Точное совпадение

    class Meta:
        model = MedicalInstitution
        fields = ['name', 'city', 'region', 'institution_type']

class DoctorFilter(django_filters.FilterSet):
    specialty = django_filters.CharFilter(field_name='specialty__name', lookup_expr='exact')
    gender = django_filters.CharFilter(field_name='user__gender', lookup_expr='exact')
    min_age = django_filters.NumberFilter(method='filter_min_age', label='Минимальный возраст')
    max_age = django_filters.NumberFilter(method='filter_max_age', label='Максимальный возраст')
    experience_years = django_filters.CharFilter(field_name='experience_years', lookup_expr='icontains')

    def filter_min_age(self, queryset, name, value):
        today = datetime.date.today()
        birth_date = today - relativedelta(years=value)
        return queryset.filter(user__date_of_birth__lte=birth_date)
    
    def filter_max_age(self, queryset, name, value):
        today = datetime.date.today()
        birth_date = today - relativedelta(years=value)
        return queryset.filter(user__date_of_birth__gte=birth_date)
    
    class Meta:
        model = Doctor
        fields = ['specialty']