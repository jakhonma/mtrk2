from django.db import models
from django.core.validators import FileExtensionValidator
from utils.generator import code_generator
from utils.directory import directory_path


class Sender(models.Model):
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name


class Notice(models.Model):
    pdf = models.FileField(upload_to=directory_path, validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return self.pdf.name


class Letter(models.Model):
    class Process(models.TextChoices):
        CREATED = 'CREATED', 'CREATED'
        CHANNEL_DIRECTOR = 'CHANNEL_DIRECTOR', 'CHANNEL_DIRECTOR'
        ARCHIVE_DIRECTOR = 'ARCHIVE_DIRECTOR', 'ARCHIVE_DIRECTOR'
        ARCHIVE_EMPLOYEE = 'ARCHIVE_EMPLOYEE', 'ARCHIVE_EMPLOYEE'
        FINISHED = 'FINISHED', 'FINISHED'
        CANCEL = 'CANCEL', 'CANCEL'

    title = models.CharField(max_length=200, null=True, blank=True)
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE)
    sender = models.ForeignKey(Sender, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    process = models.CharField(max_length=18, choices=Process.choices, default=Process.CREATED)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def channel_directory(self):
        if self.process == self.Process.CREATED:
            self.process = self.Process.CHANNEL_DIRECTOR
            self.save()

    def archive_directory(self):
        if self.process == self.Process.CHANNEL_DIRECTOR:
            self.process = self.Process.ARCHIVE_DIRECTOR
            self.save()

    def archive_employee(self):
        if self.process == self.Process.ARCHIVE_DIRECTOR:
            self.process = self.Process.ARCHIVE_EMPLOYEE
            self.save()
        else:
            pass

    def archive_finished(self):
        if self.process == self.Process.ARCHIVE_EMPLOYEE:
            self.process = self.Process.FINISHED
            self.save()

    def cancel(self):
        self.process = self.Process.CANCEL
        self.is_active = False
        self.save()

    def __str__(self):
        return self.title


