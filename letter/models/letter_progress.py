from django.db import models
from letter.models import Letter
from authentication.models import User
from utils.choices import LetterAction
from django.core.exceptions import ValidationError


class LetterProgress(models.Model):
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name='progress_logs'
    )
    sent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rel_sents"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rel_recipients"
    )
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
        ordering = ['-letter__updated']
        constraints = [
            models.UniqueConstraint(
                fields=("letter", "recipient"), name="unique_progress"
            ),
        ]
    
    def clean(self):
        if LetterProgress.objects.filter(
            letter=self.letter,
            recipient=self.recipient,
            sent=self.sent,
            letter__progress=self.letter.progress
        ).exclude(id=self.id).exists():
            raise ValidationError("letter, recipient, va letter progress unique.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Letter {self.pk}:by {self.letter.pk}"
