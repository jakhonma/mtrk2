from rest_framework import serializers
from letter.serializers import LetterSerializer


class NotificationSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    message = serializers.CharField(read_only=True)
    letter = LetterSerializer(read_only=True)
    is_read = serializers.BooleanField(default=False)