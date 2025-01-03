from rest_framework import viewsets, generics, permissions, response
from authentication.serializers import GroupSerializer, PermissionSerializer
from django.contrib.auth.models import Group, Permission
from controller.serializers import ChannelSerializer
from controller.models import Channel


class ChannelListAPIView(generics.ListAPIView):
    """
        List a queryset.
    """
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (permissions.AllowAny,)
