from django.db import models
from django.core.validators import FileExtensionValidator
from utils.directory import directory_path
from letter.models import Sender
from controller.models import Channel


class Progress(models.TextChoices):
    CREATED = 'CREATED', 'Created'
    CHANNEL_DIRECTOR = 'CHANNEL_DIRECTOR', 'Channel Director'
    ARCHIVE_DIRECTOR = 'ARCHIVE_DIRECTOR', 'Archive Director'
    ARCHIVE_EMPLOYEE = 'ARCHIVE_EMPLOYEE', 'Archive Employee'
    FINISHED = 'FINISHED', 'Finished'
    CANCELED = 'CANCELED', 'Cancelled'


class Letter(models.Model):
    title = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    pdf = models.FileField(
        upload_to=directory_path, 
        validators=[
                FileExtensionValidator(['pdf'])
            ]
    )
    channel = models.ForeignKey(
        Channel, 
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        'authentication.User', 
        on_delete=models.CASCADE, 
        related_name='created_letters'
    )
    current_user = models.ForeignKey(
        'authentication.User', 
        on_delete=models.SET_NULL, 
        related_name='processing_letters',
        null=True,
        blank=True
    )
    progress = models.CharField(
        max_length=18, 
        choices=Progress.choices, 
        default=Progress.CREATED
    )
    description = models.CharField(max_length=300)
    explain = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    # def channel_directory(self):
    #     if self.process == Progress.CREATED:
    #         self.process = Progress.CHANNEL_DIRECTOR
    #         self.save()

    # def archive_directory(self):
    #     if self.process == Progress.CHANNEL_DIRECTOR:
    #         self.process = Progress.ARCHIVE_DIRECTOR
    #         self.save()

    # def archive_employee(self):
    #     if self.process == Progress.ARCHIVE_DIRECTOR:
    #         self.process = Progress.ARCHIVE_EMPLOYEE
    #         self.save()
    #     else:
    #         pass

    # def archive_finished(self):
    #     if self.process == Progress.ARCHIVE_EMPLOYEE:
    #         self.process = Progress.FINISHED
    #         self.is_active = False
    #         self.save()

    # def cancel(self):
    #     self.process = Progress.CANCELED
    #     self.is_active = False
    #     self.save()

    def __str__(self):
        return self.title
