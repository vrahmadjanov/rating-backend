from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from a_base.models import Advantage, Subscription


class AdvantageAdmin(TranslationAdmin):
    list_display = ('name_ru', 'name_tg', 'description_short')
    search_fields = ('name_ru', 'name_tg', 'description_ru', 'description_tg')
    fieldsets = (
        (_('Русская версия'), {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        (_('Таджикская версия'), {
            'fields': ('name_tg', 'description_tg'),
            'classes': ('collapse',)
        }),
    )

    def description_short(self, obj):
        # Показываем русское описание в списке
        return obj.description_ru[:100] + '...' if obj.description_ru and len(obj.description_ru) > 100 else obj.description_ru
    description_short.short_description = _('Краткое описание')


class SubscriptionAdvantageInline(admin.TabularInline):
    model = Subscription.advantages.through
    extra = 1
    verbose_name = _('Преимущество')
    verbose_name_plural = _('Преимущества подписки')

class SubscriptionAdmin(TranslationAdmin):
    list_display = ('name_ru', 'name_tg', 'price_formatted', 'duration_days', 'is_active', 'advantages_count')
    list_filter = ('is_active', 'duration_days')
    search_fields = ('name_ru', 'name_tg', 'description_ru', 'description_tg')
    readonly_fields = ('advantages_list',)
    filter_horizontal = ('advantages',)
    fieldsets = (
        (_('Основные параметры'), {
            'fields': ('is_active', 'price', 'duration_days')
        }),
        (_('Русская версия'), {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        (_('Таджикская версия'), {
            'fields': ('name_tg', 'description_tg'),
            'classes': ('collapse',)
        }),
        (_('Преимущества'), {
            'fields': ('advantages_list', 'advantages')
        }),
    )
    inlines = (SubscriptionAdvantageInline,)

    def price_formatted(self, obj):
        return f"{obj.price} TJS"
    price_formatted.short_description = _('Цена')

    def advantages_count(self, obj):
        return obj.advantages.count()
    advantages_count.short_description = _('Кол-во преимуществ')

    def advantages_list(self, obj):
        advantages = obj.get_advantages_list()
        if not advantages:
            return _('Нет преимуществ')
        return format_html('<ul>{}</ul>', 
            ''.join([f'{adv} ' for adv in advantages]))
    advantages_list.short_description = _('Список преимуществ')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('advantages')

admin.site.register(Advantage, AdvantageAdmin)
admin.site.register(Subscription, SubscriptionAdmin)