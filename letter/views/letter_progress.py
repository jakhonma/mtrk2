from rest_framework import views, permissions, response, generics
from letter.serializers import LetterProgressSerializer
from letter.models import LetterProgress, Progress


class LetterProgressAPIView(generics.ListAPIView):
    """
    List a queryset.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(changed_by=user, letter__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     letter_progres = LetterProgress.objects.filter(changed_by=user, letter__is_active=True)
    #     # .exclude(letter__progress=Progress.CANCELED)
    #     serialazer = LetterProgressSerializer(letter_progres, many=True)
    #     return response.Response(serialazer.data)


class LetterProgressUpdateAPIView(generics.UpdateAPIView):
    """
        Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)
