from rest_framework import serializers
from letter.models import LetterProgress
from letter.serializers import LetterListSerializer


class LetterProgressSerializer(serializers.ModelSerializer):
    letter = LetterListSerializer()
    class Meta:
        model = LetterProgress
        fields = '__all__'
