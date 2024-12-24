from helper.models import Mtv, Format, Language, Region
from helper.serializers import AbstractClassSerializer
from rest_framework import serializers


class MtvSerializer(AbstractClassSerializer):
    def create(self, validated_data):
        return Mtv.objects.create(**validated_data)


class FormatSerializer(AbstractClassSerializer):
    def create(self, validated_data):
        return Format.objects.create(**validated_data)


class RegionSerializer(AbstractClassSerializer):
    def create(self, validated_data):
        return Region.objects.create(**validated_data)


class LanguageSerializer(AbstractClassSerializer):
    def create(self, validated_data):
        return Language.objects.create(**validated_data)


class HelperListSerializer(serializers.Serializer):
    """
        Mtv, Region, Language va Format Listni qaytaradigan Serializer
    """
    mtvs = MtvSerializer(many=True)
    formats = FormatSerializer(many=True)
    regions = RegionSerializer(many=True)
    languages = LanguageSerializer(many=True)