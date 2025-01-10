from rest_framework import permissions, response, generics, status, exceptions
from letter.serializers import LetterProgressSerializer, LetterProgressCreateApprovedSerializer, LetterProgressCreateRejectedSerializer
from letter.models import LetterProgress, Progress
from django.db.models import Q
from utils.choices import UserRole


class LetterProgressUserAllAPIView(generics.ListAPIView):
    """
        List a queryset.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(Q(recipient=user) | Q(sent=user), letter__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     letter_progres = LetterProgress.objects.filter(changed_by=user, letter__is_active=True)
    #     # .exclude(letter__progress=Progress.CANCELED)
    #     serialazer = LetterProgressSerializer(letter_progres, many=True)
    #     return response.Response(serialazer.data)


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
        queryset = LetterProgress.objects.filter(recipient=user, letter__is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressCreateApprovedAPIView(generics.CreateAPIView):
    serializer_class = LetterProgressCreateApprovedSerializer
    queryset = LetterProgress.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.context['user'] = user
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class LetterProgressCreateRejectedAPIView(generics.CreateAPIView):
    serializer_class = LetterProgressCreateRejectedSerializer
    queryset = LetterProgress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)    
