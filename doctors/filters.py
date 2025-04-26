# doctors/filters.py
import django_filters
from dateutil.relativedelta import relativedelta
import datetime
from .models.doctors import Doctor

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