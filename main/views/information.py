from django.db.models import Count, Case, When, IntegerField, Avg
from django.db.models.functions import Coalesce
from rest_framework import (
    status, filters, permissions, 
    pagination, response, generics
)
from main.serializers import InformationSerializer, InformationCreateUpdateSerializer
from main.models import Information
from django_filters.rest_framework import DjangoFilterBackend
from utils.media import delete_media
from controller.permissions import IsOwnerPermission, IsGroupUserPermission
from django.shortcuts import get_object_or_404
from main.filters import InformationFilter
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication


# class InformationViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = InformationSerializer
#     pagination_class = pagination.LimitOffsetPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     ordering_fields = ['region', 'language', 'year']
#     search_fields = ['title', 'brief_data', 'summary', 'mtv_index', 'location_on_server']
#     filterset_fields = [
#         'fond__department__name',
#         'category__parent__fond__department__name',
#         'category__fond__name',
#         'category__parent__name',
#         'category__name',
#         'region__name',
#         'year',
#         'month',
#         'day',
#         'is_serial'
#     ]
#
#     def get_queryset(self):
#         if not self.request.user.has_perm("can_confidential"):
#             queryset = Information.objects\
#             .filter(confidential=False)\
#             .annotate(
#                 rating=Avg('ratings__rating')
#             )\
#             .order_by('-created')
#         else:
#             queryset = Information.objects.all()\
#             .annotate(
#                 rating=Avg('ratings__rating')
#             )\
#             .order_by('-created')
#
#         return queryset
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         rating = instance.ratings.all().aggregate(rating=Avg("rating", default=0))
#         instance.rating = rating["rating"]
#         serializer = self.get_serializer(instance)
#         return response.Response(serializer.data)


class InformationListAPIView(generics.ListAPIView):
    serializer_class = InformationSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['region', 'language', 'year']
    search_fields = ['title', 'brief_data', 'summary', 'mtv_index', 'location_on_server']
    filterset_class = InformationFilter

    def get_queryset(self):
        if not self.request.user.has_perm("can_confidential"):
            queryset = (Information.objects.filter(confidential=False).annotate(
                rating=Avg('ratings__rating'),
                serial_count=Count(
                    Case(
                        When(is_serial=True, then='serials'),  # is_serial=True bo'lsa serialsni hisobla
                        output_field=IntegerField()
                    ),
                    distinct=True)
            ).order_by('-created'))
        else:
            queryset = Information.objects.annotate(
                rating=Avg('ratings__rating'),
                serial_count=Count(
                    Case(
                        When(is_serial=True, then='serials'),  # is_serial=True bo'lsa serialsni hisobla
                        output_field=IntegerField()
                    ),
                    distinct=True)
            ).order_by('-created')
        return queryset


class InformationRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = (JWTAuthentication, )
    serializer_class = InformationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.has_perm("can_confidential"):
            queryset = Information.objects.filter(confidential=False)
        else:
            queryset = Information.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        rating = instance.ratings.all().aggregate(rating=Avg("rating", default=0))
        instance.rating = rating["rating"]
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class InformationCreateAPIView(generics.CreateAPIView):
    """
        Information creation API view
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    queryset = Information.objects.all()
    serializer_class = InformationCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class InformationUpdateAPIView(generics.UpdateAPIView):
    """
        Update a model instance.
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    queryset = Information.objects.all()
    serializer_class = InformationCreateUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class InformationDestroyAPIView(generics.DestroyAPIView):
    """
        Destroy a model instance.
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    serializer_class = InformationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Information,
            pk=kwargs['pk']
        )
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        if instance.poster is not None:
            name = instance.poster.image.name
            delete_media(name)
        cadre = instance.information.all()
        if cadre is not None:
            for item in cadre:
                delete_media(item.image.name)
        with transaction.atomic():
            instance.delete()
