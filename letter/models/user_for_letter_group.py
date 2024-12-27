from django.db import models
from letter.models import Letter
from authentication.models import User


class Chat(models.Model):
    letter = models.OneToOneField(Letter, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class LetterMessage(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    MESSAGE_TYPES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image')
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.CharField(max_length=300)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default=TEXT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.content} from {self.sender}"


class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.chat}"
