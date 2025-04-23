from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только администратору или самому пользователю.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ если пользователь - администратор или запрашивает свой профиль
        return request.user.is_staff or obj == request.user

class IsAdminOrReadOnlyForSelf(permissions.BasePermission):
    """
    Разрешение, которое позволяет:
    - Полный доступ администратору
    - Чтение любому аутентифицированному пользователю
    - Запись только для своего профиля
    """
    def has_permission(self, request, view):
        # Разрешаем доступ всем аутентифицированным пользователям
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешаем полный доступ администратору
        if request.user.is_staff:
            return True
            
        # Разрешаем чтение всем аутентифицированным пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Разрешаем запись только для своего профиля
        return obj == request.user