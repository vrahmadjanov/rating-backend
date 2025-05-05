from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение, которое позволяет:
    - Чтение всем аутентифицированным пользователям
    - Запись только администраторам
    """
    def has_permission(self, request, view):
        # Разрешаем чтение для всех аутентифицированных
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Разрешаем запись только администраторам
        return request.user and request.user.is_staff
    
class IsDoctorOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем аутентифицированным
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        
        # Редактирование только владельцу профиля
        return obj.user == request.user or request.user.is_staff
    
class IsDoctorOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Разрешаем чтение для всех аутентифицированных пользователей
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Разрешаем запись только администраторам или пользователям в группе 'Доктор'
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.groups.filter(name='Доктор').exists())
        )