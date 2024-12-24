from django.db.models import Count, Case, When, IntegerField, Avg
from rest_framework import generics, status, response, permissions
from rest_framework.exceptions import ValidationError

from main.models import Bookmark, Information, Rating
from main.serializers import BookmarkSerializer, BookmarkListSerializer, InformationSerializer


class BookmarkListAPIView(generics.ListAPIView):
    """
        List a queryset.
    """
    serializer_class = InformationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = request.user
        information_queryset = Information.objects.filter(
            rel_information__user=user
        ).annotate(
                rating=Avg('ratings__rating'),
                serial_count=Count(
                    Case(
                        When(is_serial=True, then='serials'),
                        output_field=IntegerField()
                    ),
                    distinct=True)
            )
        # lst = []
        # info = []
        # queryset = Bookmark.objects.filter(user=user)
        # for bookmark in queryset:
        #     if bookmark.information is not None and not self.request.user.has_perm("can_confidential") and bookmark.information.confidential:
        #         pass
        #     else:
        #         info.append(bookmark.information)
        # for information in info:
        #     rating = Rating.objects.filter(information=information).aggregate(rating=Avg('rating'))
        #     information.rating = rating['rating']
        #     lst.append(information)
        serializer = self.get_serializer(information_queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkListIdAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Bookmark.objects.filter(user=user).values_list('information', flat=True)
        return response.Response({"data": queryset}, status=status.HTTP_200_OK)


class BookmarkCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookmarkDestroyAPIView(generics.DestroyAPIView):
    """
        Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        user = request.user
        information_id = kwargs['information_id']
        try:
            instance = Bookmark.objects.get(information_id=information_id, user=user)
            self.perform_destroy(instance)
        except Bookmark.DoesNotExist:
            raise ValidationError('Bookmark not found.')
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
