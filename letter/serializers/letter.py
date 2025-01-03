from rest_framework import serializers
from letter.models import Letter
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class LetterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = '__all__'


class LetterCreateUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    letter_type = serializers.CharField(max_length=20)
    pdf = serializers.FileField(
        # read_only=True,
        validators=[
            FileExtensionValidator(['pdf'])
        ]
    )
    channel_id = serializers.IntegerField()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    current_user_id = serializers.IntegerField(allow_null=True, required=False)
    progress = serializers.ChoiceField(choices=Letter._meta.get_field('progress').choices, default=Letter._meta.get_field('progress').default)
    description = serializers.CharField(max_length=800)
    is_active = serializers.BooleanField(default=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField()
    updated = serializers.DateTimeField(allow_null=True, required=False)

    def validate(self, data):
        now = timezone.now()
        if 'end_date' in data and data['end_date'] and data['end_date'] < now:
            raise serializers.ValidationError("Tugash sanasi boshlanish sanasidan oldin bo'lishi mumkin emas.")
        if str(data).endswith('.pdf'):
            raise serializers.ValidationError("PDF file yuboring!")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['current_user_id'] = user.id
        # validated_data['pdf'] = self.context['pdf']
        return Letter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
