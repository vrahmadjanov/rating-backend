from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Поля, отображаемые в списке пользователей
    list_display = [
        'phone_number', 
        'first_name', 
        'last_name', 
        'email',
        'city', 
        'subscription', 
        'is_active', 
    ]

    # Фильтры в правой части админки
    list_filter = [
        'is_staff', 
        'is_active', 
        'gender', 
        'date_joined'
    ]

    # Поля для поиска
    search_fields = [
        'email', 
        'first_name', 
        'last_name', 
        'phone_number', 
        'inn',
        'city'
    ]

    # Сортировка по умолчанию
    ordering = ['subscription']

    # Группировка полей на странице редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {
            'fields': (
                'first_name', 
                'last_name', 
                'middle_name', 
                'phone_number', 
                'gender',
                'subscription', 
                'city', 
                'inn',
                'date_of_birth', 
                'profile_picture', 
                'subscription_start_date',
                'subscription_end_date'
            )
        }),
        ('Права доступа', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            )
        }),
        ('Важные даты', {
            'fields': (
                'last_login', 
                'date_joined'
            )
        }),
    )

    # Поля для добавления нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password1', 
                'password2', 
                'first_name', 
                'last_name', 
                'middle_name',
                'date_of_birth', 
                'phone_number', 
                'gender',
                'subscription',
                'city', 
                'inn',
                'profile_picture'
            )
        }),
    )

# Регистрация модели CustomUser с кастомной админкой
admin.site.register(CustomUser, CustomUserAdmin)