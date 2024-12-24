from rest_framework import serializers
from main.models import Cadre


class CadreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField()
    information_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['information_id'] = self.context['information_id']
        return Cadre.objects.create(**validated_data)
