from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import (
    ArchiveDirectorUser, 
    ArchiveEmployeeUser, 
    ChannelEmployeeUser, 
    ChannelDirectorUser, 
    ChannelAssistantUser
)


class Channel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    director = models.ForeignKey(ChannelDirectorUser, on_delete=models.CASCADE, related_name='rel_channel_director')
    assistant = models.ForeignKey(ChannelAssistantUser, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ManyToManyField(ChannelEmployeeUser, blank=True, related_name='rel_channel_employeis')
    code = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Archive(models.Model):
    name = models.CharField(max_length=100)
    director = models.ForeignKey(ArchiveDirectorUser, on_delete=models.CASCADE, related_name='rel_archive_director')
    employee = models.ManyToManyField(ArchiveEmployeeUser, blank=True, related_name='rel_archive_employeis')
    letter_work = models.ManyToManyField(ArchiveEmployeeUser, blank=True, related_name='rel_letter_work')

    def clean(self):
        # Agar modelda yozuv bo'lsa va yangi yozuv kiritilsa, xatolik qaytariladi
        if Archive.objects.exists() and not self.pk:  # self.pk mavjud emasligi yangi yozuv degan ma'noda
            raise ValidationError("Faqat bitta Archive yozuvi bo'lishi mumkin!")

    def save(self, *args, **kwargs):
        self.clean()  # clean metodini chaqirish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
