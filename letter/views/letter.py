from rest_framework import generics, response, permissions, status, parsers
from letter.models import Letter, LetterProgress
from letter.serializers import LetterCreateUpdateSerializer
from django.db import transaction
from letter.permissions import IsChannelEmployeePermission


class LetterCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    permission_classes = [permissions.IsAuthenticated, IsChannelEmployeePermission]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class = LetterCreateUpdateSerializer
    queryset = Letter.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LetterCreateUpdateSerializer(data=request.data)
        serializer.context['request'] = request
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            letter = serializer.save()
            LetterProgress.objects.create(
                letter=letter,
                recipient=request.user
            )
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LetterListAPIView(generics.ListAPIView):
    """
        List a queryset.    
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
