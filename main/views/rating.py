from rest_framework import generics, response, status, permissions
from rest_framework.exceptions import ValidationError
from main.models import Rating
from main.serializers import RatingCreateUpdateSerializer, RatingSerializer
from django.db import transaction


class RatingRetrieveAPIView(generics.RetrieveAPIView):
    """
        Retrieve a model instance.
    """
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        information_id = kwargs.get('information_id')
        instance = Rating.objects.filter(information_id=information_id, user=user)
        data = {
            "is_rating": False,
            "rating": None,
        }

        if instance.exists():
            serializer = self.get_serializer(instance.first())
            data = {
                "is_rating": True,
                "rating": serializer.data,
            }
            return response.Response(data=data, status=status.HTTP_200_OK)
        return response.Response(data=data, status=status.HTTP_200_OK)


class RatingCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    queryset = Rating.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = RatingCreateUpdateSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = {
                "is_rating": True,
                "rating": serializer.data,
            }
        return response.Response(data=data, status=status.HTTP_201_CREATED, headers=headers)


class RatingUpdateAPIView(generics.UpdateAPIView):
    """
        Update a model instance.
    """
    serializer_class = RatingCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        partial = kwargs.pop('partial', False)
        try:
            instance = Rating.objects.get(pk=kwargs['pk'], user=user)
            serializer = RatingCreateUpdateSerializer(
                instance=instance,
                data=request.data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            data = {
                "is_rating": True,
                "rating": serializer.data,
            }
            return response.Response(data=data)
        except Rating.DoesNotExist:
            raise ValidationError('Rating does not exist')
