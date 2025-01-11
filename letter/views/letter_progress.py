from rest_framework import permissions, response, generics, status, exceptions
from letter.serializers import LetterProgressSerializer, LetterProgressCreateApprovedSerializer, LetterProgressCreateRejectedSerializer
from letter.models import LetterProgress, Progress
from django.db.models import Q, functions, Value, CharField
from utils.choices import UserRole, Progress


class LetterProgressUserAllAPIView(generics.ListAPIView):
    """
        List a queryset.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(Q(recipient=user), letter__is_active=True).annotate(
            combined_field=functions.Concat('letter', Value('_'), 'recipient', output_field=CharField())
        ).order_by('combined_field').distinct('combined_field')
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressUserSentAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(sent=user, letter__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressUserRecipientAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.exclude(letter__created_by=user).filter(recipient=user, letter__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressCreateApprovedAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressCreateApprovedSerializer
    queryset = LetterProgress.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.context['user'] = user
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class LetterProgressCreateRejectedAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressCreateRejectedSerializer
    queryset = LetterProgress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)    
