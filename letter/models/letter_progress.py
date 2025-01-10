from django.db import models
from letter.models import Letter, Progress
from authentication.models import User
from utils.choices import LetterAction


class LetterProgress(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='progress_logs')
    # status = models.CharField(max_length=50, choices=Progress.choices)
    sent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="rel_sents")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rel_recipients")
    action = models.CharField(
        max_length=50,
        choices=LetterAction.choices,
        null=True,
        blank=True
    )
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated']

    def __str__(self):
        return f"Letter {self.letter.pk}: {self.status} by {self.changed_by.username}"
