from rest_framework import serializers
from main.models import Bookmark
from main.serializers.information import InformationSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class BookmarkListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    information = InformationSerializer()


class BookmarkSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    information_id = serializers.IntegerField()

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(
            user_id=self.context["user_id"],
            **validated_data
        )
        return bookmark

    def validate(self, attrs):
        category = Bookmark(**attrs)
        try:
            category.clean()
        except DjangoValidationError as e:
            raise DRFValidationError({"msg": e.message})
        return attrs
