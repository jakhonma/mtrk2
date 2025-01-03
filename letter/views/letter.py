from rest_framework import viewsets, views, generics, response, permissions, status, parsers
from letter.models import Letter, Notification, LetterAction, LetterProgress, Progress
from letter.serializers import LetterCreateUpdateSerializer
from letter.task import add_letter
from django.db import transaction


class LetterCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class = LetterCreateUpdateSerializer
    queryset = Letter.objects.all()

    def create(self, request, *args, **kwargs):
        # pdf = add_letter(request.data)
        serializer = LetterCreateUpdateSerializer(data=request.data)
        # serializer.context['pdf'] = pdf
        serializer.context['request'] = request
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            letter = serializer.save()
            LetterProgress.objects.create(
                letter=letter,
                status=Progress.CREATED,
                changed_by=request.user,
                action=LetterAction.APPROVED
            )
            Notification.objects.create(
                recipient=request.user,
                letter=letter,
                message=f"Sizda yangi xat!"
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
