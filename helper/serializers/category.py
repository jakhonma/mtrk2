from helper.models import Category
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from helper.serializers import FondSerializer


class NestedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'fond', 'parent']

    def validate(self, attrs):
        category = Category(**attrs)
        try:
            category.clean()
        except DjangoValidationError as e:
            raise DRFValidationError({"msg": e.message})
        return attrs


class InformationCategorySerializer(serializers.ModelSerializer):
    parent = NestedCategorySerializer(required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'fond', 'parent']


class CategorySerializer(serializers.ModelSerializer):
    children = NestedCategorySerializer(many=True, read_only=True)
    fond = FondSerializer()

    class Meta:
        model = Category
        fields = ['id', 'name', 'fond', 'children']

