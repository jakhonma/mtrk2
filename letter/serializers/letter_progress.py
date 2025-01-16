from rest_framework import serializers, exceptions
from letter.models import LetterProgress
from letter.serializers import LetterListSerializer
from utils.choices import LetterAction, Progress, UserRole
from controller.models import Archive
from authentication.models import ArchiveEmployeeUser
from letter.task import edit_channel_director, edit_archive_director
from django.core.files.storage import default_storage


class LetterProgressSerializer(serializers.ModelSerializer):
    letter = LetterListSerializer()

    class Meta:
        model = LetterProgress
        fields = '__all__'


class LetterProgressCreateRejectedSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action == LetterAction.APPROVED or letter_progress.action == LetterAction.REJECTED:
                letter_progress.action = LetterAction.REJECTED
                letter_progress.save()
                letter = letter_progress.letter
                letter.progress = Progress.CANCELED
                letter.save()
                return LetterProgress.objects.create(
                    letter_id=letter.id,
                    sent_id=user.id, 
                    recipient_id=letter.created_by.id, 
                    action=LetterAction.REJECTED, 
                    **validated_data
                )
            else:
                raise exceptions.ValidationError({"msg": "xatolik"})
        except LetterProgress.DoesNotExist:
                raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateApprovedSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)
    recipient_id = serializers.IntegerField(allow_null=True)
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
        letter_progress_id = validated_data.pop('letter_progress_id')

        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                if user.role == UserRole.CHANNEL_EMPLOYEE:
                    letter = letter_progress.letter
                    letter.progress = progress_mapping.get('CREATED')
                    letter_progress.action = LetterAction.APPROVED
                    letter_progress.save()
                    letter.save()
                    return LetterProgress.objects.create(
                        letter_id=letter.pk,
                        sent_id=user.pk,
                        **validated_data
                    )
                elif user.role == UserRole.CHANNEL_DIRECTOR or user.role == UserRole.CHANNEL_ASSISTANT:
                    archive = Archive.objects.all().first()
                    letter_progress.action = LetterAction.APPROVED
                    validated_data.pop('recipient_id')
                    letter = letter_progress.letter
                    letter.progress = progress_mapping.get(letter.progress)
                    letter.pdf, delete_pdf = edit_channel_director(letter, user=user)
                    letter_progress.save()
                    letter.save()
                    if default_storage.exists(delete_pdf):
                        default_storage.delete(delete_pdf)
                    return LetterProgress.objects.create(
                        letter_id=letter.pk, 
                        sent_id=user.pk, 
                        recipient_id=archive.director.pk,
                        action=LetterAction.APPROVED
                    )
                elif user.role == UserRole.ARCHIVE_DIRECTOR:
                    archive = Archive.objects.all().first()
                    letter_progress.action = LetterAction.APPROVED
                    validated_data.pop('recipient_id')
                    letter = letter_progress.letter
                    letter.progress = progress_mapping.get(letter.progress)
                    letter.pdf, delete_pdf = edit_archive_director(letter, user=user)
                    letter_progress.save()
                    letter.save()
                    if default_storage.exists(delete_pdf):
                        default_storage.delete(delete_pdf)
                    return LetterProgress.objects.create(
                        letter_id=letter.pk, 
                        sent_id=user.pk, 
                        recipient=archive.employee.all().first(),
                        action=LetterAction.APPROVED
                    )
                elif user.role == UserRole.ARCHIVE_EMPLOYEE:
                    pass
                else:
                    raise exceptions.ValidationError({"msg": "Tasdiqlash uchun user topilmadi!"})
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateChannelEmployeeSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)
    recipient_id = serializers.IntegerField()
    action = serializers.CharField()

    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')

        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                letter = letter_progress.letter
                letter.channel_directory()
                letter_progress.action = LetterAction.APPROVED
                letter_progress.save()
                return LetterProgress.objects.create(
                    letter_id=letter.pk, 
                    sent_id=user.id, 
                    **validated_data
                )
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateChannelDirectorOrChannelAssistantSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)
    recipient_id = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                archive = Archive.objects.all().first()
                letter_progress.action = LetterAction.APPROVED
                validated_data.pop('recipient_id')
                letter = letter_progress.letter
                letter.archive_directory()
                letter.pdf, delete_pdf = edit_channel_director(letter, user=user)
                letter_progress.save()
                if default_storage.exists(delete_pdf):
                    default_storage.delete(delete_pdf)
                return LetterProgress.objects.create(
                    letter_id=letter.pk, 
                    sent_id=user.pk, 
                    recipient_id=archive.director.pk,
                    action=LetterAction.APPROVED
                )
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateArchiveDirectorSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)
    recipient_ids = serializers.PrimaryKeyRelatedField(
        queryset=ArchiveEmployeeUser.objects.all(),
        many=True
    )

    def create(self, validated_data):
        new_letter_progress = None
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is not None:
                letter = letter_progress.letter
                letter.archive_employee()
                recipient_ids = validated_data.pop('recipient_ids')
                letter.pdf, delete_pdf = edit_archive_director(
                    letter=letter,
                    user=user
                )
                letter_progress.save()
                if default_storage.exists(delete_pdf):
                    default_storage.delete(delete_pdf)
                for item in recipient_ids:
                    new_letter_progress = LetterProgress.objects.create(
                        letter_id=letter.pk, 
                        sent_id=user.pk, 
                        recipient_id=item, 
                        action=LetterAction.APPROVED 
                    )
                return new_letter_progress
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateArchiveEmployeeSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                letter = letter_progress.letter
                letter.archive_finished()
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})
