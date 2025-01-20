from rest_framework import serializers, exceptions
from letter.models import LetterProgress
from letter.serializers import LetterListSerializer
from utils.choices import LetterAction, Progress, UserRole
from controller.models import Archive
from authentication.models import ArchiveEmployeeUser
from letter.task import edit_channel_director, edit_archive_director
from utils.delete_pdf_file import delete_pdf_file
from django.db import transaction

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
            if letter_progress.action is None:
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


# class LetterProgressCreateApprovedSerializer(serializers.Serializer):
#     letter_progress_id = serializers.IntegerField(required=False)
#     recipient_id = serializers.IntegerField(allow_null=True)
#     action = serializers.CharField()

#     def create(self, validated_data):
#         progress_mapping = {
#             'CREATED': 'CHANNEL_DIRECTOR',
#             'CHANNEL_DIRECTOR': 'ARCHIVE_DIRECTOR',
#             'ARCHIVE_DIRECTOR': 'ARCHIVE_EMPLOYEE',
#             'ARCHIVE_EMPLOYEE': 'FINISHED',  # FINISHED bosqichi uchun oluvchi yo'q
#         }
#         user = self.context['user']
#         letter_progress_id = validated_data.pop('letter_progress_id')

#         try:
#             letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
#             if letter_progress.action is None:
#                 if user.role == UserRole.CHANNEL_EMPLOYEE:
#                     letter = letter_progress.letter
#                     letter.progress = progress_mapping.get('CREATED')
#                     letter_progress.action = LetterAction.APPROVED
#                     letter_progress.save()
#                     letter.save()
#                     return LetterProgress.objects.create(
#                         letter_id=letter.pk,
#                         sent_id=user.pk,
#                         **validated_data
#                     )
#                 elif user.role == UserRole.CHANNEL_DIRECTOR or user.role == UserRole.CHANNEL_ASSISTANT:
#                     archive = Archive.objects.all().first()
#                     letter_progress.action = LetterAction.APPROVED
#                     validated_data.pop('recipient_id')
#                     letter = letter_progress.letter
#                     letter.progress = progress_mapping.get(letter.progress)
#                     letter.pdf, delete_pdf = edit_channel_director(letter, user=user)
#                     letter_progress.save()
#                     letter.save()
#                     delete_pdf_file(delete_pdf)
#                     return LetterProgress.objects.create(
#                         letter_id=letter.pk, 
#                         sent_id=user.pk, 
#                         recipient_id=archive.director.pk,
#                         action=LetterAction.APPROVED
#                     )
#                 elif user.role == UserRole.ARCHIVE_DIRECTOR:
#                     archive = Archive.objects.all().first()
#                     letter_progress.action = LetterAction.APPROVED
#                     validated_data.pop('recipient_id')
#                     letter = letter_progress.letter
#                     letter.progress = progress_mapping.get(letter.progress)
#                     letter.pdf, delete_pdf = edit_archive_director(letter, user=user)
#                     letter_progress.save()
#                     letter.save()
#                     delete_pdf_file(delete_pdf)
#                     new_letter_progress = LetterProgress.objects.create(
#                         letter_id=letter.pk, 
#                         sent_id=user.pk, 
#                         recipient=archive.employee.all().first(),
#                         action=LetterAction.APPROVED
#                     )
#                     return new_letter_progress
#                 elif user.role == UserRole.ARCHIVE_EMPLOYEE:
#                     pass
#                 else:
#                     raise exceptions.ValidationError({"msg": "Tasdiqlash uchun user topilmadi!"})
#             else:
#                 raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
#         except LetterProgress.DoesNotExist:
#             raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateChannelEmployeeSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)
    recipient_id = serializers.IntegerField()
    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                letter = letter_progress.letter
                letter_progress.action = LetterAction.APPROVED
                letter.channel_directory()
                letter_progress.save()
                new_letter_progress = LetterProgress.objects.create(
                    letter_id=letter.pk, 
                    sent_id=user.id, 
                    **validated_data
                )
                return new_letter_progress
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateChannelDirectorOrChannelAssistantSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                archive = Archive.objects.all().first()
                letter_progress.action = LetterAction.APPROVED
                letter = letter_progress.letter
                letter.pdf, delete_pdf = edit_channel_director(letter, user=user)
                letter.archive_directory()
                letter_progress.letter = letter
                letter_progress.save()
                new_letter_progress = LetterProgress.objects.create(
                    letter_id=letter.pk, 
                    sent_id=user.pk, 
                    recipient_id=archive.director.pk
                )
                delete_pdf_file(delete_pdf)
                return new_letter_progress
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})


class LetterProgressCreateArchiveDirectorSerializer(serializers.Serializer):
    letter_progress_id = serializers.IntegerField(required=False)
    recipient_ids = serializers.PrimaryKeyRelatedField(
        queryset=ArchiveEmployeeUser.objects.all(),
        many=True,
        required=False
    )
    def create(self, validated_data):
        user = self.context['user']
        letter_progress_id = validated_data.pop('letter_progress_id')
        try:
            letter_progress = LetterProgress.objects.get(pk=letter_progress_id)
            if letter_progress.action is None:
                letter_progress.action = LetterAction.APPROVED
                letter_progress_list = []
                letter = letter_progress.letter
                recipient_ids = validated_data.pop('recipient_ids')
                print(recipient_ids[0])
                
                # try:
                #     with transaction.atomic():
                letter.pdf, delete_pdf = edit_archive_director(
                    letter,
                    user=user
                )
                letter.archive_employee()
                letter_progress.letter = letter
                letter_progress.save()
                delete_pdf_file(delete_pdf)
                for item in recipient_ids:
                    letter_progress_list.append(
                        LetterProgress(
                            letter_id=letter.pk, 
                            sent_id=user.pk, 
                            recipient=item, 
                    ))
                letter_progress_list = LetterProgress.objects.bulk_create(letter_progress_list)
                return letter_progress_list[0]
                # except Exception as error:
                #     raise error
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
                print(letter_progress)
                letter_progress.action = LetterAction.APPROVED
                print(letter_progress)
                letter = letter_progress.letter
                letter.finished()
                print('letter', letter)
                letter_progress.save()
                new_letter_progress = LetterProgress.objects.create(
                    letter_id=letter.pk, 
                    sent_id=user.pk, 
                    recipient_id=letter.created_by.pk
                )
                print(new_letter_progress)
                return new_letter_progress
            else:
                raise exceptions.ValidationError({"msg": "Bu Xat tasdiqlangan!"})
        except LetterProgress.DoesNotExist:
            raise exceptions.ValidationError({'msg': f"Xat topilmadi"})
