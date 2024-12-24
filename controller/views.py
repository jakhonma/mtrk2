from rest_framework import viewsets, generics, permissions
from controller.serializers import GroupSerializer, PermissionSerializer
from django.contrib.auth.models import Group, Permission


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (permissions.AllowAny,)
