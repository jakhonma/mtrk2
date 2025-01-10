from rest_framework import serializers, exceptions
from letter.models import LetterProgress, Letter
from letter.serializers import LetterListSerializer
from controller.serializers import ChannelSerializer
from utils.choices import LetterAction, Progress, UserRole
from authentication.models import User
from controller.models import Archive
from letter.task import edit_channel_derictor


class LetterProgressSerializer(serializers.ModelSerializer):
    letter = LetterListSerializer()
    class Meta:
        model = LetterProgress
        fields = '__all__'


class LetterProgressCreateApprovedSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField(required=False)
    action = serializers.CharField()

    def create(self, validated_data):
        progress_mapping = {
            'CREATED': 'CHANNEL_DIRECTOR',
            'CHANNEL_DIRECTOR': 'ARCHIVE_DIRECTOR',
            'ARCHIVE_DIRECTOR': 'ARCHIVE_EMPLOYEE',
            'ARCHIVE_EMPLOYEE': 'FINISHED',  # FINISHED bosqichi uchun oluvchi yo'q
        }
        user = self.context['user']
        action = validated_data.pop('action')
        letter_progress_id = validated_data.get('letter_progress_id')

        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            letter_progress.action = action
            letter_progress.save()
            letter = letter_progress.letter
            letter.progress = progress_mapping.get(letter.progress)
            if user.role == UserRole.CHANNEL_EMPLOYEE:
                new_letter_progress = LetterProgress.objects.create(sent_id=user.id, **validated_data)
            elif user.role == UserRole.CHANNEL_DIRECTOR or user.role == UserRole.CHANNEL_ASSISTANT:
                archive = Archive.objects.all().first()
                letter.pdf = edit_channel_derictor(letter.pdf, data=None)
                new_letter_progress = LetterProgress.objects.create(sent_id=user.id, recipient_id=archive.director.id, **validated_data)
            elif user.role == UserRole.ARCHIVE_DIRECTOR:
                pass
            elif user.role == UserRole.ARCHIVE_EMPLOYEE:
                pass
            else:
                pass
            letter.save()
            return new_letter_progress
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateRejectedSerializer(serializers.Serializer):
    letter_id = serializers.IntegerField()
    letter_progress_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField(required=False)
    action = serializers.CharField()

    def create(self, validated_data):
        user = self.context['user']
        action = validated_data.pop('action')
        letter_id = validated_data.get('letter_id')
        letter_progress_id = validated_data.get('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            letter_progress.action = action
            letter_progress.save()
            letter = Letter.objects.get(pk=letter_id)
            letter.progress = Progress.CANCELED
            letter.save()
            
            return LetterProgress.objects.create(
                send_id=user.id, 
                recipient_id=letter.created_by.id, 
                action=action, 
                **validated_data
            )
        except LetterProgress.DoesNotExist:
                raise exceptions.ValidationError({'msg': f"Xat topilmadi"})
