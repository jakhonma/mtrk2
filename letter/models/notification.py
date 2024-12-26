from django.db import models
from letter.models import Letter
from authentication.models import User


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(null=True, blank=True)
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"