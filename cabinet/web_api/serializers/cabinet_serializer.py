from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from cabinet.models import Cabinet, Cell


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
        if time_start < timezone.now():
            raise serializers.ValidationError({'errorMessage': 'Thời gian bắt đầu phải lớn hơn thời gian hiện tại'})
        if time_start + timedelta(minutes=30) >= time_end:
            raise serializers.ValidationError({'errorMessage': 'Khoảng thời gian không hợp lệ'})
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
