from django.db import models
from authentication.models import ArchiveDirectorUser, ArchiveEmployeeUser, ChannelEmployeeUser, ChannelDirectorUser


class Channel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    director = models.ForeignKey(ChannelDirectorUser, on_delete=models.CASCADE, related_name='rel_channel_director')
    employee = models.ManyToManyField(ChannelEmployeeUser, blank=True, related_name='rel_channel_employeis')

    def __str__(self):
        return self.name


class Archive(models.Model):
    name = models.CharField(max_length=100)
    director = models.ForeignKey(ArchiveDirectorUser, on_delete=models.CASCADE, related_name='rel_archive_director')
    employee = models.ManyToManyField(ArchiveEmployeeUser, blank=True, related_name='rel_archive_employeis')

    def __str__(self):
        return self.name
