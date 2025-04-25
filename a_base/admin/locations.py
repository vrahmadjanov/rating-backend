from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from a_base.models import Region, District

@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    list_display = ('code', 'name_ru', 'name_tg')
    list_display_links = ('code', 'name_ru')
    search_fields = ('code', 'name_ru', 'name_tg')
    ordering = ('code',)
    
    fieldsets = (
        (None, {
            'fields': ('code',),
        }),
        ('Название региона', {
            'fields': ('name_ru', 'name_tg'),
            'classes': ('wide', 'extrapretty'),
        }),
    )

@admin.register(District)
class DistrictAdmin(TranslationAdmin):
    list_display = ('code', 'name_ru', 'name_tg', 'region_display')
    list_display_links = ('code', 'name_ru')
    list_filter = ('region',)
    search_fields = ('code', 'name_ru', 'name_tg', 'region__name_ru', 'region__name_tg')
    ordering = ('code',)
    raw_id_fields = ('region',)
    
    fieldsets = (
        (None, {
            'fields': ('code', 'region'),
        }),
        ('Название района', {
            'fields': ('name_ru', 'name_tg'),
            'classes': ('wide', 'extrapretty'),
        }),
    )
    
    def region_display(self, obj):
        return f"{obj.region.name_ru} ({obj.region.code})"
    region_display.short_description = 'Регион'
    region_display.admin_order_field = 'region__code'

