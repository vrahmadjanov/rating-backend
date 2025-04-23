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