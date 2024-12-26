from rest_framework import viewsets, views, generics, response, permissions
from letter.models import Sender
from letter.serializers import SenderSerializer
from controller.permissions import IsGroupUserPermission


class SenderViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    queryset = Sender.objects.all()
    serializer_class = SenderSerializer
