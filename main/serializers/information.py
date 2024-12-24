from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from utils.relationship import add_many_to_many, edit_many_to_many
from helper.models import Mtv, Region, Language, Format
from main.serializers import PosterSerializer
from django.core.validators import MinValueValidator, MaxValueValidator
from main.models import Information
from datetime import date
from helper.serializers import (
    FondSerializer, 
    MtvSerializer, 
    RegionSerializer,
    LanguageSerializer, 
    FormatSerializer, 
    InformationCategorySerializer
)


class InformationSerializer(serializers.ModelSerializer):
    serial_count = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(required=True)
    fond = FondSerializer(required=True)
    category = InformationCategorySerializer(required=False)
    mtv = MtvSerializer(many=True, read_only=True)
    region = RegionSerializer(many=True, read_only=True)
    language = LanguageSerializer(many=True, read_only=True)
    format = FormatSerializer(many=True, read_only=True)
    poster = PosterSerializer(required=False, allow_null=True)

    # def get_average_rating(self, obj):
    #     return obj.average_rating

    class Meta:
        model = Information
        fields = [
            'id', 'title', 'fond', 'category',
            'mtv', 'region', 'language', 'format',
            'poster', 'mtv_index', 'location_on_server',
            'color', 'material', 'duration', 'year', 'month',
            'day', 'restorat', 'restoration', 'confidential',
            'brief_data', 'summary', 'is_serial', 'created'
            , 'rating', 'serial_count'
        ]


class InformationCreateUpdateSerializer(serializers.Serializer):
    """
        Information Create va Update qiladigan Serializer
    """
    COLOURED = 'coloured'
    WHITE_BLACK = 'white-black'
    COLORS = (
        (COLOURED, 'coloured'),
        (WHITE_BLACK, 'white-black')
    )

    ETHER = 'ether'
    PRIMARY = 'primary'
    MATERIAL = (
        (ETHER, 'ether'),
        (PRIMARY, 'primary')
    )

    id = serializers.IntegerField(read_only=True)
    fond_id = serializers.IntegerField(write_only=True)
    fond = FondSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    category = InformationCategorySerializer(read_only=True)
    mtv_ids = serializers.PrimaryKeyRelatedField(
        queryset=Mtv.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    mtv = MtvSerializer(
        many=True,
        read_only=True
    )
    region_ids = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        many=True,
        required=False
    )
    region = RegionSerializer(
        many=True,
        read_only=True
    )
    language_ids = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        many=True,
        required=False
    )
    language = LanguageSerializer(
        many=True,
        read_only=True
    )
    format_ids = serializers.PrimaryKeyRelatedField(
        queryset=Format.objects.all(),
        many=True,
        required=False
    )
    format = FormatSerializer(many=True, read_only=True)
    title = serializers.CharField(max_length=255)
    mtv_index = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    location_on_server = serializers.CharField(max_length=250, allow_null=True, allow_blank=True)
    color = serializers.ChoiceField(choices=COLORS, default=COLOURED)
    material = serializers.ChoiceField(choices=MATERIAL, default=ETHER)
    duration = serializers.TimeField(allow_null=True)
    year = serializers.IntegerField(validators=[
        MinValueValidator(1920, message="Yilni tug'ri kiriting?"),
        MaxValueValidator(int(date.today().year), message="Yilni tug'ri kiriting?")
    ], allow_null=True)
    month = serializers.IntegerField(validators=[
        MinValueValidator(1, message="Oyni tug'ri kiriting?"),
        MaxValueValidator(12, message="Oyni tug'ri kiriting?")
    ], allow_null=True)
    day = serializers.IntegerField(validators=[
        MinValueValidator(1, message="Kunni tug'ri kiriting?"),
        MaxValueValidator(31, message="Kunni tug'ri kiriting?")
    ], allow_null=True)
    restorat = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    restoration = serializers.BooleanField(default=False)
    confidential = serializers.BooleanField(default=False)
    brief_data = serializers.CharField(max_length=3000, allow_null=True, allow_blank=True)
    summary = serializers.CharField(max_length=3000, allow_null=True, allow_blank=True)
    is_serial = serializers.BooleanField(default=False)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        mtvs = validated_data.pop('mtv_ids')
        regions = validated_data.pop('region_ids')
        languages = validated_data.pop('language_ids')
        formats = validated_data.pop('format_ids')

        employee = self.context['request'].user
        information = Information.objects.create(employee=employee, **validated_data)

        # information = Information.objects.create(**validated_data)
        add_many_to_many(information.mtv, mtvs)
        add_many_to_many(information.region, regions)
        add_many_to_many(information.language, languages)
        add_many_to_many(information.format, formats)

        return information

    def update(self, instance, validated_data):
        mtvs = validated_data.pop('mtv_ids')
        regions = validated_data.pop('region_ids')
        languages = validated_data.pop('language_ids')
        formats = validated_data.pop('format_ids')

        employee = self.context['request'].user
        if not employee.is_superuser and instance.employee != employee:
            raise PermissionDenied("Siz faqat o'zingizning ma'lumotlaringizni yangilashingiz mumkin.")

        instance.title = validated_data.get('title', instance.title)
        instance.fond_id = validated_data.get('fond_id', instance.fond.id)
        instance.category_id = validated_data.get('category_id', instance.category.id)
        instance.mtv_index = validated_data.get('mtv_index', instance.mtv_index)
        instance.location_on_server = validated_data.get('location_on_server', instance.location_on_server)
        instance.color = validated_data.get('color', instance.color)
        instance.material = validated_data.get('material', instance.material)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.year = validated_data.get('year', instance.year)
        instance.month = validated_data.get('month', instance.month)
        instance.day = validated_data.get('day', instance.day)
        instance.restorat = validated_data.get('restorat', instance.restorat)
        instance.restoration = validated_data.get('restoration', instance.restoration)
        instance.confidential = validated_data.get('confidential', instance.confidential)
        instance.brief_data = validated_data.get('brief_data', instance.brief_data)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.is_serial = validated_data.get('is_serial', instance.is_serial)
        instance.save()

        edit_many_to_many(instance.mtv, mtvs)
        edit_many_to_many(instance.region, regions)
        edit_many_to_many(instance.language, languages)
        edit_many_to_many(instance.format, formats)

        return instance
