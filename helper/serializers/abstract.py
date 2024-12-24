from rest_framework import serializers


class AbstractClassSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        return instance
