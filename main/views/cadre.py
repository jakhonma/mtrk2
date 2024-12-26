from rest_framework import status, filters, permissions, response, parsers, generics
from main.serializers import CadreSerializer
from main.models import Cadre
from utils.media import delete_media
from controller.permissions import IsOwnerPermission, IsGroupUserPermission
from django.shortcuts import get_object_or_404
from django.db import transaction


class CadreListAPIView(generics.ListAPIView):
    """
        Cadrelar Listini qaytaradi
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CadreSerializer

    def get_queryset(self):
        queryset = Cadre.objects.filter(information_id=self.kwargs['information_id'])
        return queryset


class CadreCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    serializer_class = CadreSerializer
    parser_classes = (parsers.MultiPartParser,)

    def get_queryset(self):
        queryset = Cadre.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        information_id = kwargs['information_id']
        serializer = self.get_serializer(
            data=request.data,
            context={'information_id': information_id}
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CadreDeleteAPIView(generics.DestroyAPIView):
    """
        Destroy a model instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    queryset = Cadre.objects.all()
    serializer_class = CadreSerializer

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Cadre, pk=self.kwargs['pk'])
        delete_media(instance.image.name)
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()
