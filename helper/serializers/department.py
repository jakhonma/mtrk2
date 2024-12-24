from typing import Any
from helper.models import Department
from rest_framework import serializers
from helper.serializers import AbstractClassSerializer


class DepartmentSerializer(AbstractClassSerializer):
    def create(self, validated_data):
        return Department.objects.create(**validated_data)

    def validate_name(self, attr: Any):
        if Department.objects.filter(name=attr).exists():
            raise serializers.ValidationError("Department with this name already exists.")
        return attr
