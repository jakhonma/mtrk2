from rest_framework import serializers
from main.models import Information, Serial
from rest_framework.exceptions import ValidationError


class SerialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    information_id = serializers.IntegerField(required=False)
    part = serializers.IntegerField()
    duration = serializers.TimeField()

    def create(self, validated_data):
        validated_data['information_id'] = self.context['information_id']
        return Serial.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.part = validated_data.get('part', instance.part)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()
        return instance

    def validate(self, attrs):
        information_id = self.context['information_id']
        information = Information.objects.get(pk=information_id)
        if not information.is_serial:
            raise ValidationError({"msg": "Serialga qushing"})
        return attrs
