from helper.models import Fond
from rest_framework import serializers


class FondSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    department_id = serializers.IntegerField()
    name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Fond.objects.create(**validated_data)
