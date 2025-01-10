from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'ADMIN'
    ARCHIVE_DIRECTOR = 'ARCHIVE_DIRECTOR', 'ARCHIVE_DIRECTOR'
    CHANNEL_DIRECTOR = 'CHANNEL_DIRECTOR', 'CHANNEL_DIRECTOR'
    ARCHIVE_EMPLOYEE = 'ARCHIVE_EMPLOYEE', 'ARCHIVE_EMPLOYEE'
    CHANNEL_ASSISTANT = 'CHANNEL_ASSISTANT', 'CHANNEL_ASSISTANT'
    CHANNEL_EMPLOYEE = 'CHANNEL_EMPLOYEE', 'CHANNEL_EMPLOYEE'
    LOW_USER = 'LOW_USER', 'LOW_USER'


class LetterAction(models.TextChoices):
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class Progress(models.TextChoices):
    CREATED = 'CREATED', 'Created'
    CHANNEL_DIRECTOR = 'CHANNEL_DIRECTOR', 'Channel Director'
    ARCHIVE_DIRECTOR = 'ARCHIVE_DIRECTOR', 'Archive Director'
    ARCHIVE_EMPLOYEE = 'ARCHIVE_EMPLOYEE', 'Archive Employee'
    FINISHED = 'FINISHED', 'Finished'
    CANCELED = 'CANCELED', 'Cancelled'


class LetterType(models.TextChoices):
    NOTICE = 'notice', 'Notice'  # Bildirishnoma
    APPLICATION = 'application', 'Application' #Ariza xati
    # OFFICIAL = 'official', 'Official'  # Rasmiy xat
    # PERSONAL = 'personal', 'Personal'  # Shaxsiy xat
    # INVITATION = 'invitation', 'Invitation'  # Taklifnoma
    # REQUEST = 'request', 'Request'  # So'rov xati
    # OTHER = 'other', 'Other'  # Boshqa
