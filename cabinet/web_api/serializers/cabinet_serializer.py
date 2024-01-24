from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from cabinet.models import Cabinet, Cell
from exe201_backend.common.utils import Utils


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'controller_id', 'cabinetType_id', 'description', 'start_using_date', 'height', 'width',
                  'depth', 'status', 'image_link', 'virtual_cabinet_id']


class EmptyCellsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ['hash_code', 'cell_index', 'width', 'height', 'depth']


class EmptyCellsRequestSerializer(serializers.Serializer):
    cabinet_id = serializers.IntegerField(required=True)
    time_start = serializers.DateTimeField(required=True)
    time_end = serializers.DateTimeField(required=True)

    def validate(self, data):
        time_start = data['time_start']
        time_end = data['time_end']
        valid_messages = Utils.validate_order_time(time_start, time_end)
        if not valid_messages:
            raise serializers.ValidationError({
                'message': valid_messages
            })
        return data


class CabinetNearbySerializer(serializers.Serializer):
    location_detail = serializers.CharField()
    ward_name = serializers.CharField()
    cabinet_id = serializers.IntegerField()
    district_name = serializers.CharField()
    province_name = serializers.CharField()
    empty_cell = serializers.IntegerField()
    cabinet_name = serializers.CharField()

class CabinetInformationSerializer(serializers.Serializer):
    location_name = serializers.CharField()
    location_detail = serializers.CharField()
    width = serializers.FloatField()
    height = serializers.FloatField()
    depth = serializers.FloatField()
    empty_cell = serializers.IntegerField()
    description = serializers.CharField()
    cabinet_type = serializers.CharField()
