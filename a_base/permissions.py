from rest_framework import permissions

class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ на чтение всем, а изменение только админам.
    """
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if view.action == 'subscribe' and request.method == 'POST':
            return request.user and request.user.is_authenticated
        
        # Для небезопасных методов проверяем аутентификацию и права
        if not request.user or not request.user.is_authenticated:
            return False  # Будет 403 Forbidden
        
        return request.user.is_staff
    
class IsOwner(permissions.BasePermission):
    """Разрешает доступ на чтение, редактирование и удаление владельцу объекта"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Проверяем, является ли пользователь владельцем объекта
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'patient'):
            return obj.patient.user == request.user
        elif hasattr(obj, 'doctor'):
            return obj.doctor.user == request.user
        return False
    
    def has_permission(self, request, view):
        # Для списковых запросов разрешаем только аутентифицированным пользователям
        return request.user and request.user.is_authenticated
        