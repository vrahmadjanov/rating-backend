from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (Doctor, Service, Language, MedicalCategory, 
                     Workplace, Education, UserLanguage, LanguageLevel, 
                     Schedule)

admin.site.register(Doctor)
admin.site.register(Service)
admin.site.register(Language)
admin.site.register(UserLanguage)
admin.site.register(LanguageLevel)
admin.site.register(MedicalCategory)
admin.site.register(Workplace)
admin.site.register(Education)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor_info', 'compact_weekly_schedule', 'appointment_interval')
    list_select_related = ('workplace__doctor__user',)
    search_fields = (
        'workplace__doctor__user__first_name',
        'workplace__doctor__user__last_name',
        'workplace__clinic__name'
    )
    ordering = ('workplace__doctor__user__last_name',)
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'workplace',
                'appointment_interval',
            )
        }),
        (_('Расписание по дням недели'), {
            'fields': (
                ('monday_start', 'monday_end'),
                ('tuesday_start', 'tuesday_end'),
                ('wednesday_start', 'wednesday_end'),
                ('thursday_start', 'thursday_end'),
                ('friday_start', 'friday_end'),
                ('saturday_start', 'saturday_end'),
                ('sunday_start', 'sunday_end'),
            ),
            'classes': ('wide',)
        }),
    )

    def doctor_info(self, obj):
        """Отображает информацию о враче и месте работы."""
        if obj.workplace and obj.workplace.doctor:
            return f"{obj.workplace.doctor.user.get_full_name} ({obj.workplace.clinic.name})"
        return "-"
    doctor_info.short_description = _('Врач (место работы)')
    doctor_info.admin_order_field = 'workplace__doctor__user__last_name'

    def compact_weekly_schedule(self, obj):
        """Компактное отображение недельного расписания в текстовом формате."""
        days = [
            ('Пн', obj.monday_start, obj.monday_end),
            ('Вт', obj.tuesday_start, obj.tuesday_end),
            ('Ср', obj.wednesday_start, obj.wednesday_end),
            ('Чт', obj.thursday_start, obj.thursday_end),
            ('Пт', obj.friday_start, obj.friday_end),
            ('Сб', obj.saturday_start, obj.saturday_end),
            ('Вс', obj.sunday_start, obj.sunday_end),
        ]
        
        schedule = []
        for day, start, end in days:
            if start and end:
                schedule.append(f"{day}: {start.strftime('%H:%M')}-{end.strftime('%H:%M')}")
        
        return ", ".join(schedule) if schedule else _("Нет рабочих дней")
    compact_weekly_schedule.short_description = _('Рабочие дни')

    def get_fieldsets(self, request, obj=None):
        """Динамическое изменение fieldsets."""
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = (
                (_('Текущее расписание'), {
                    'fields': ('current_schedule_display',),
                    'classes': ('collapse',)
                }),
            ) + fieldsets
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        """Определяет поля только для чтения."""
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('current_schedule_display',)
        return readonly_fields

    def current_schedule_display(self, obj):
        """Отображение текущего расписания (только для чтения)."""
        return self.compact_weekly_schedule(obj)
    current_schedule_display.short_description = _('Текущее расписание')

    def get_queryset(self, request):
        """Оптимизация запросов к БД."""
        return super().get_queryset(request).select_related(
            'workplace__doctor__user',
            'workplace__clinic'
        )