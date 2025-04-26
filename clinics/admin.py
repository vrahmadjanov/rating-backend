from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from .models import Clinic, ClinicType

class ClinicTypeAdmin(TranslationAdmin):
    list_display = ('name_ru', 'name_tg')
    search_fields = ('name_ru', 'name_tg')
    list_display_links = ('name_ru',)


@admin.register(Clinic)
class ClinicAdmin(TranslationAdmin):
    list_display = (
        'name_display',
        'clinic_type_display',
        'district_display',
        'phone_number',
        'email',
        'location_link'
    )
    list_filter = ('clinic_type', 'district')
    search_fields = (
        'name_ru', 'name_tg',
        'address_ru', 'address_tg',
        'phone_number', 'email'
    )
    list_select_related = ('clinic_type', 'district')
    raw_id_fields = ('district',)
    filter_horizontal = ()
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'name_ru', 'name_tg',
                'clinic_type',
                'address_ru', 'address_tg',
                'district'
            )
        }),
        (_('Контактные данные'), {
            'fields': (
                'phone_number',
                'email',
                'website'
            )
        }),
        (_('Геоданные'), {
            'fields': (
                'country',
                ('latitude', 'longitude'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Кастомные методы для отображения
    def name_display(self, obj):
        return obj.name
    name_display.short_description = _('Название')
    name_display.admin_order_field = 'name_ru'
    
    def clinic_type_display(self, obj):
        return obj.clinic_type.name
    clinic_type_display.short_description = _('Тип клиники')
    clinic_type_display.admin_order_field = 'clinic_type__name_ru'
    
    def district_display(self, obj):
        return obj.district.name
    district_display.short_description = _('Район')
    district_display.admin_order_field = 'district__name'

    def location_link(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '<a href="https://yandex.ru/maps/?pt={},{}&z=18&l=map" target="_blank">🌍 Карта</a>',
                obj.longitude, obj.latitude
            )
        return "-"
    location_link.short_description = _('Карта')

admin.site.register(ClinicType, ClinicTypeAdmin)