from rest_framework import permissions

class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ на чтение всем, а изменение только админам.
    """
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для небезопасных методов проверяем аутентификацию и права
        if not request.user or not request.user.is_authenticated:
            return False  # Будет 403 Forbidden
        
        return request.user.is_staff