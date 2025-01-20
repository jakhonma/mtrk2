from rest_framework import serializers
from controller.models import Channel, Archive
from authentication.serializers import UserSerializer, UserResponsibleSerializer


class ChannelSerializer(serializers.ModelSerializer):
    director = UserSerializer(read_only=True)
    assistant = UserSerializer(read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'director', 'assistant', 'phone', 'employee', 'code']


class ArchiveSerializer(serializers.ModelSerializer):
    employee = UserResponsibleSerializer(read_only=True, many=True)

    class Meta:
        model = Archive
        fields = ['id', 'name', 'director', 'employee']

