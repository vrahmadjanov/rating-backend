from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import Service, ServicePlace

@admin.register(ServicePlace)
class ServicePlaceAdmin(TranslationAdmin):
    list_display = ('name_ru', 'name_tg')
    list_display_links = ('name_ru',)
    search_fields = ('name_ru', 'name_tg',)
    ordering = ('name_ru',)
    

@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('name_ru', 'name_tg', 'description_ru', 'description_tg', 'service_place_display',)
    list_display_links = ('name_ru',)
    list_filter = ('service_place',)
    search_fields = ('name_ru', 'service_place_name_ru',)
    ordering = ('name_ru',)
    raw_id_fields = ('service_place',)

    
    def service_place_display(self, obj):
        return f"{obj.service_place.name_ru} ({obj.service_place.id})"
    service_place_display.short_description = 'Место предоставления услуги'
    service_place_display.admin_order_field = 'service_place__name_ru'

