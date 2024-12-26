from rest_framework import status, permissions, response, generics
from main.serializers import SerialSerializer
from main.models import Serial, Information
from controller.permissions import IsOwnerPermission, IsGroupUserPermission
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from utils import timedelta, not_serial
from django.db import transaction


class SerialListAPiView(generics.ListAPIView):
    """
        List a queryset.
    """
    serializer_class = SerialSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = get_object_or_404(
            Information,
            pk=kwargs['information_id'],
            is_serial=True
        ).serials.all()

        not_ = not_serial.not_serials(queryset)

        total = queryset.aggregate(
            count=Count('id'),
            time_sum=Sum('duration')
        )
        time_delta = total.get('time_sum')
        total = {
            "count": total.get("count"),
            "time_sum": timedelta.times(time_delta),
            "not_serials": not_
        }
        serializer = self.get_serializer(queryset, many=True)
        result = {
            "serials": serializer.data,
            "total": total
        }
        return response.Response(result)


class SerialRetrieveAPIView(generics.RetrieveAPIView):
    """
        Retrieve a model instance.
    """
    serializer_class = SerialSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instance = Serial.objects.get(
            information_id=kwargs['information_id'],
            pk=pk
        )
        # instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class SerialCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    serializer_class = SerialSerializer

    def get_queryset(self):
        return Serial.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'information_id': kwargs['information_id']}
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


class SerialUpdateAPIView(generics.UpdateAPIView):
    """
        Update a model instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)
    serializer_class = SerialSerializer
    queryset = Serial.objects.all()

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        partial = kwargs.pop('partial', False)
        instance = Serial.objects.get(
            information_id=kwargs['information_id'],
            pk=pk
        )
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={
                'information_id': kwargs['information_id']
            }
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return response.Response(serializer.data)


class SerialDestroyAPIView(generics.DestroyAPIView):
    """
        Destroy a model instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsGroupUserPermission)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instance = Serial.objects.get(
            information_id=kwargs['information_id'],
            pk=pk
        )
        with transaction.atomic():
            instance.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
