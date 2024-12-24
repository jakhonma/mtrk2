from rest_framework import serializers
from main.models import Poster


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = ['pk', 'image']
