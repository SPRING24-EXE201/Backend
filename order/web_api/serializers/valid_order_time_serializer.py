from datetime import timedelta
from uuid import UUID

from dateutil import parser
from django.utils import timezone as tz
from rest_framework import serializers

from cabinet.models import CampaignCabinet, CostVersion, Cabinet, Cell
from exe201_backend.common.constants import SystemConstants
from exe201_backend.common.utils import Utils


class ValidOrderTimeRequestSerializer(serializers.Serializer):
    hash_code = serializers.UUIDField()
    time_start = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    time_end = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def validate(self, data):
        time_start = data['time_start']
        time_end = data['time_end']
        valid_messages = Utils.validate_order_time(time_start, time_end)
        if valid_messages is not None:
            raise serializers.ValidationError({
                'message': valid_messages
            })
        return data


class ValidOrderTimeRequestListSerializer(serializers.ListSerializer):
    child = ValidOrderTimeRequestSerializer()

    def validate(self, data):
        converted_data = {}
        for item in data:
            if converted_data.get(item.get('hash_code')):
                raise serializers.ValidationError({
                    'message': 'Trùng lặp thông tin ô tủ'
                })
            converted_data[item.get('hash_code')] = {
                'time_start': item.get('time_start'),
                'time_end': item.get('time_end')
            }
        try:
            data = Utils.check_valid_cells(converted_data)
        except Cell.DoesNotExist:
            raise serializers.ValidationError({
                'message': 'Không tìm thấy ô tủ!'
            })
        return data


class ValidOrderSerializer(serializers.Serializer):
    hash_code = serializers.UUIDField()
    location_detail = serializers.SerializerMethodField()
    depth = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()
    total_cost = serializers.SerializerMethodField()

    def get_total_cost(self, data):
        total_cost = 0
        error_message = None
        try:
            total_cost = Utils.calc_total_cost_in_order_detail(data['hash_code'], data['time_start'], data['time_end'])
        except Cell.DoesNotExist:
            error_message = 'Không tìm thấy ô tủ!'
        except (CampaignCabinet.DoesNotExist, CostVersion.DoesNotExist):
            error_message = 'Không thể tính toán, vui lòng thử lại sau!'
        if error_message is not None:
            raise serializers.ValidationError({
                'message': error_message
            })
        return total_cost

    def get_location_detail(self, data):
        location_detail = ''
        try:
            cabinet = Cabinet.objects.get(id=data.get('cabinet_id'),
                                          status=True)
            location_detail = cabinet.controller.location.location_detail
        except Cabinet.DoesNotExist:
            pass
        return location_detail
