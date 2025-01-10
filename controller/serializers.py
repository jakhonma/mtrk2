from rest_framework import serializers
from controller.models import Channel
from authentication.serializers import UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    director = UserSerializer(read_only=True)
    assistant = UserSerializer(read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'director', 'assistant', 'phone', 'employee', 'code']

