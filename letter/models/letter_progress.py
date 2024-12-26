from django.db import models
from letter.models import Letter, Progress
from authentication.models import User


class LetterAction(models.TextChoices):
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class LetterProgress(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='progress_logs')
    status = models.CharField(max_length=50, choices=Progress.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(
        max_length=50,
        choices=LetterAction.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Letter {self.letter.pk}: {self.status} by {self.changed_by.username}"