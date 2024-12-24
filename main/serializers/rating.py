from rest_framework import serializers
from main.models import Rating


class RatingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(read_only=True)


class RatingCreateUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    information_id = serializers.IntegerField()
    rating = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context['request'].user
        return Rating.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance
