from django.db import models
from django.core.validators import FileExtensionValidator
from utils.directory import directory_path
from letter.models import Sender
from controller.models import Channel
from utils.choices import Progress, LetterType


class Letter(models.Model):
    letter_type = models.CharField(
        max_length=12, 
        choices=LetterType.choices,
        default=LetterType.NOTICE
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
        'authentication.ChannelEmployeeUser', 
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
    description = models.CharField(max_length=800)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    def channel_directory(self):
        if self.progress == Progress.CREATED:
            self.progress = Progress.CHANNEL_DIRECTOR
            self.save()
            return True
        return False

    def archive_directory(self):
        if self.progress == Progress.CHANNEL_DIRECTOR:
            self.progress = Progress.ARCHIVE_DIRECTOR
            self.save()
            return True
        return False

    def archive_employee(self):
        if self.progress == Progress.ARCHIVE_DIRECTOR:
            self.progress = Progress.ARCHIVE_EMPLOYEE
            self.save()
            return True
        return False

    def archive_finished(self):
        if self.progress == Progress.ARCHIVE_EMPLOYEE:
            self.progress = Progress.FINISHED
            self.is_active = False
            self.save()
            return True
        return False

    def cancel(self):
        self.progress = Progress.CANCELED
        self.is_active = False
        self.save()
    
    def __str__(self):
        return self.letter_type
