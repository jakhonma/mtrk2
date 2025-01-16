from rest_framework.permissions import BasePermission
from authentication.models import UserRole


class IsChannelEmployeePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == UserRole.CHANNEL_EMPLOYEE

    def has_permission(self, request, view):
        user = request.user
        return user.role == UserRole.CHANNEL_EMPLOYEE


class IsChannelDirectorOrArchiveDirector(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == UserRole.ARCHIVE_DIRECTOR \
            or user.role == UserRole.CHANNEL_DIRECTOR \
            or user.role == UserRole.CHANNEL_ASSISTANT
    
    def has_permission(self, request, view):
        user = request.user
        return user.role == UserRole.ARCHIVE_DIRECTOR \
            or user.role == UserRole.CHANNEL_DIRECTOR \
            or user.role == UserRole.CHANNEL_ASSISTANT
