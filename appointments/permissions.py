from rest_framework import permissions

class IsAdminOrPatientOwner(permissions.BasePermission):
    """
    Разрешение, которое позволяет админам видеть все записи,
    а пациентам - только свои собственные.
    """
    def has_permission(self, request, view):
        # Админы имеют доступ ко всем действиям
        if request.user.is_staff:
            return True
        # Пациенты могут только читать свои записи
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Админы имеют полный доступ
        if request.user.is_staff:
            return True
        # Пациенты могут видеть только свои записи
        return obj.patient == request.user