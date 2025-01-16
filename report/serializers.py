from rest_framework import serializers
from helper.models import Mtv
from report.models import Report, InfoItem


# class InfoItemListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         items = [InfoItem(**item) for item in validated_data]
#         return InfoItem.objects.bulk_create(items)
#
#
# class InfoItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=False)
#     name = serializers.CharField(max_length=255)
#     duration = serializers.TimeField()
#
#     class Meta:
#         list_serializer_class = InfoItemListSerializer


class InfoItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    duration = serializers.TimeField()


class InfoItemListSerializer(serializers.ListSerializer):
    child = InfoItemSerializer()

    def create(self, validated_data):
        items = [InfoItem(**item) for item in validated_data]
        return InfoItem.objects.bulk_create(items)


class ReportSerializer(serializers.Serializer):
    reports = InfoItemListSerializer()
    fond_id = serializers.IntegerField()
    send_mtv_id = serializers.IntegerField(required=False, allow_null=True)
    received_mtv_id = serializers.IntegerField(required=False, allow_null=True)
    number = serializers.IntegerField(default=0)
    dvd_number = serializers.IntegerField(default=0)
    info = serializers.CharField(max_length=455)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        reports_data = validated_data.pop('reports', [])
        employee = self.context['request'].user
        report = Report.objects.create(employee=employee, **validated_data)

        for item in reports_data:
            item['report'] = report
        InfoItemListSerializer().create(reports_data)

        return report

    def update(self, instance, validated_data):
        reports_data = validated_data.pop('reports')
        instance.fond_id = validated_data.get('fond_id', instance.fond_id)
        instance.send_mtv_id = validated_data.get('send_mtv_id', instance.send_mtv_id)
        instance.received_mtv_id = validated_data.get('received_mtv_id', instance.received_mtv_id)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.number = validated_data.get('number', instance.number)
        instance.dvd_number = validated_data.get('dvd_number', instance.dvd_number)
        instance.info = validated_data.get('info', instance.info)

        reports_data = validated_data.get('reports', [])
        existing_items = {item.id: item for item in instance.reports.all()}

        for item_data in reports_data:
            item_id = item_data.get('id', None)
            if item_id and item_id in existing_items:
                existing_item = existing_items.pop(item_id)
                existing_item.name = item_data.get('name', existing_item.name)
                existing_item.duration = item_data.get('duration', existing_item.duration)
                existing_item.save()
            else:
                item_data['report'] = instance
                InfoItem.objects.create(**item_data)

        for item in existing_items.values():
            item.delete()

        return instance
