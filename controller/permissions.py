from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from authentication.models import User


class IsGroupUserPermission(BasePermission):
    METHOD = {
        'GET': 'view_',
        'POST': 'add_',
        'PUT': 'change_',
        'DELETE': 'delete_'
    }

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        class_name = view.get_queryset().model.__name__.lower()
        code_name = self.METHOD.get(request.method) + class_name
        try:
            is_exists = request.user.groups.permissions.filter(codename=code_name).exists()
            if is_exists:
                return True
        except Exception as e:
            raise ValidationError({"error": e, "msg": "Bu ViewSetga kirishga ruxsat yuq"})
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        class_name = obj.__class__.__name__.lower()
        code_name = self.METHOD.get(request.method) + class_name
        try:
            is_exists = request.user.groups.permissions.filter(codename=code_name).exists()
            if is_exists:
                return True
        except Exception as e:
            raise ValidationError({"error": e, "msg": "Bu ViewSetga kirishga ruxsat yuq"})
        return False


class IsOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.employee and request.user.role == User.Roles.EMPLOYEE
