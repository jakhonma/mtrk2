from rest_framework import status, permissions, response, parsers, generics
from rest_framework.exceptions import ValidationError
from main.serializers import PosterSerializer
from main.models import Information, Poster
from utils.media import delete_media
from controller.permissions import IsOwnerPermission, IsGroupUserPermission
from django.db import transaction
from django.shortcuts import get_object_or_404


class PosterCreateAPIView(generics.CreateAPIView):
    """
        Viewda ma'lum informisionga poster qo'shadi
    """
    # parser_classes = (parsers.MultiPartParser,)
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    queryset = Poster.objects.all()

    def create(self, request, *args, **kwargs):
        information_id = kwargs['information_id']
        serializer = PosterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            with transaction.atomic():
                obj = get_object_or_404(
                    Information,
                    id=information_id
                )
                obj.poster_id = serializer.data.get("pk")
                obj.save()
                return response.Response(
                    data={"msg": "Ok", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            raise ValidationError({"msg": f"Transaction failed: {e}"})


class PosterDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            with transaction.atomic():
                instance = get_object_or_404(
                    Poster,
                    pk=pk
                )
                delete_media(instance.image.name)
                instance.delete()
                return response.Response(
                    data={"msg": "Ok"},
                    status=status.HTTP_204_NO_CONTENT
                )
        except Exception as e:
            raise ValidationError({"msg": f"Transaction failed: {e}"})
