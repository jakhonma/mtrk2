from rest_framework import serializers
from helper.models import Mtv
from report.models import Report, InfoItem


class InfoItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255)
    duration = serializers.TimeField()


class ReportSerializer(serializers.Serializer):
    reports = InfoItemSerializer(many=True)
    fond_id = serializers.IntegerField()
    send_mtv_id = serializers.IntegerField()
    received_mtv_id = serializers.IntegerField()
    number = serializers.IntegerField(default=0)
    dvd_number = serializers.IntegerField(default=0)
    info = serializers.CharField(max_length=455, required=False)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        reports_data = validated_data.pop('reports')
        # employee = self.context['request'].user
        # information = Information.objects.create(employee=employee, **validated_data)
        report = Report.objects.create(**validated_data)

        for report_data in reports_data:
            InfoItem.objects.create(
                report=report,
                **report_data
            )
        return report

    def update(self, instance, validated_data):
        reports_data = validated_data.pop('reports')
        instance.fond_id = validated_data.get('fond_id', instance.fond_id)
        instance.send_mtv_id = validated_data.get('send_mtv_id', instance.send_mtv_id)
        instance.received_mtv_id = validated_data.get('received_mtv_id', instance.received_mtv_id)
        instance.number = validated_data.get('number', instance.number)
        instance.dvd_number = validated_data.get('dvd_number', instance.dvd_number)
        instance.info = validated_data.get('info', instance.info)

        for item in reports_data:
            print(item)
            info_item = InfoItem.objects.get(pk=item['id'])
            info_item.name = item['name']
            info_item.duration = item['duration']
            info_item.save()
        return instance
