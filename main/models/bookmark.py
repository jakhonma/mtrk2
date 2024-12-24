from django.db import models
from main.models import Information
from authentication.models import User


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    information = models.ForeignKey(
        Information,
        on_delete=models.CASCADE,
        related_name='rel_information',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = (('user', 'information'),)

    def __str__(self):
        return str(self.information)
