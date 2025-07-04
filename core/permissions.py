from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать только свои объекты.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user