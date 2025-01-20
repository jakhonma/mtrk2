from rest_framework import permissions, response, generics, status
from letter.serializers import (
    LetterProgressSerializer, 
    # LetterProgressCreateApprovedSerializer, 
    LetterProgressCreateRejectedSerializer,
    LetterProgressCreateChannelEmployeeSerializer,
    LetterProgressCreateChannelDirectorOrChannelAssistantSerializer,
    LetterProgressCreateArchiveDirectorSerializer,
    LetterProgressCreateArchiveEmployeeSerializer
)
from letter.models import LetterProgress
from django.db.models import functions, Value, CharField
from utils.choices import UserRole, Progress
from letter.permissions import IsChannelDirectorOrArchiveDirector


class LetterProgressUserIsReadAPIView(generics.RetrieveAPIView):
    """
        Retrieve a model instance.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LetterProgressSerializer
    queryset = LetterProgress.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class LetterProgressUserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LetterProgressSerializer


class LetterProgressUserIsReadCountAPIView(LetterProgressUserList):
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == UserRole.CHANNEL_EMPLOYEE:
            count = LetterProgress.objects.filter(
                recipient=user,
                letter__progress=Progress.CANCELED,
                letter__is_active=True,
                is_read=False).annotate(
                    combined_field=functions.Concat(
                        'letter',
                        Value('_'),
                        'recipient',
                        output_field=CharField()
                    )
                ).order_by('-combined_field').distinct('combined_field').count()
        else:
            count = LetterProgress.objects.filter(
                recipient=user,
                letter__is_active=True,
                is_read=False
            ).count()
        return response.Response(data={"letter_progress_count": count})


class LetterProgressUserAllAPIView(LetterProgressUserList):
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(
                recipient=user,
                letter__is_active=True).annotate(
                    combined_field=functions.Concat(
                        'letter',
                        Value('_'),
                        'recipient',
                        output_field=CharField()
                    )
                ).order_by('-combined_field').distinct('combined_field')
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressUserSentAPIView(LetterProgressUserList):
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(
            sent=user,
            letter__is_active=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressUserRecipientAPIView(LetterProgressUserList):
    def list(self, request, *args, **kwargs):
        user = request.user
        # if user.role == UserRole.CHANNEL_EMPLOYEE:
        #         queryset = LetterProgress.objects.filter(
        #         recipient=user,
        #         letter__is_active=True
        #     ).order_by('is_read', '-letter__updated')
        # else:
        queryset = LetterProgress.objects.exclude(letter__created_by=user).filter(
            recipient=user,
            letter__is_active=True
        ).order_by('is_read', '-letter__updated')
        # queryset = LetterProgress.objects.exclude(letter__created_by=user).filter(
        #     recipient=user,
        #     letter__is_active=True
        # ).annotate(
        #             combined_field=functions.Concat(
        #                 'letter',
        #                 Value('_'),
        #                 'recipient',
        #                 output_field=CharField()
        #             )
        #         ).order_by('-combined_field', 'is_read').distinct('combined_field')
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressUserCancelAPIView(LetterProgressUserList):
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.filter(
            sent=user,
            letter__progress=Progress.CANCELED,
            letter__is_active=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressChannelEmployeeRecipientAPIView(LetterProgressUserList):
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = LetterProgress.objects.exclude(letter__created_by=user).filter(
            recipient=user,
            letter__is_active=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class LetterProgressCreateRejectedAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsChannelDirectorOrArchiveDirector)
    serializer_class = LetterProgressCreateRejectedSerializer
    queryset = LetterProgress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class LetterProgressCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = LetterProgress.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.context['user'] = user
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


# class LetterProgressCreateApprovedAPIView(LetterProgressCreate):
#     serializer_class = LetterProgressCreateApprovedSerializer


class LetterProgressCreateChannelEmployeeAPIView(LetterProgressCreate):
    serializer_class = LetterProgressCreateChannelEmployeeSerializer


class LetterProgressCreateChannelDirectorOrChannelAssistantAPIView(LetterProgressCreate):
    serializer_class = LetterProgressCreateChannelDirectorOrChannelAssistantSerializer


class LetterProgressCreateArchiveDirectorAPIView(LetterProgressCreate):
    serializer_class = LetterProgressCreateArchiveDirectorSerializer


class LetterProgressCreateArchiveEmployeeAPIView(LetterProgressCreate):
    serializer_class = LetterProgressCreateArchiveEmployeeSerializer
