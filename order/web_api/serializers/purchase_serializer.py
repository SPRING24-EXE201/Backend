from rest_framework import serializers

from cabinet.models import Cell
from exe201_backend.common.utils import Utils


class PurchaseRequestSerializer(serializers.Serializer):
    hash_code = serializers.UUIDField(required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)

    def validate(self, data):
        time_start = data['start_date']
        time_end = data['end_date']
        # Check valid time range
        valid_messages = Utils.validate_order_time(time_start, time_end)
        if valid_messages:
            raise serializers.ValidationError({
                'message': valid_messages
            })
        return data


class PurchaseRequestListSerializer(serializers.ListSerializer):
    child = PurchaseRequestSerializer()

    def validate(self, data):
        converted_data = {}
        for item in data:
            if converted_data.get(item.get('hash_code')):
                raise serializers.ValidationError({
                    'message': 'Trùng lặp thông tin ô tủ'
                })
            converted_data[item.get('hash_code')] = {
                'time_start': item.get('start_date'),
                'time_end': item.get('end_date')
            }
        try:
            check_valid_data = Utils.check_valid_cells(converted_data)
            if len(check_valid_data.get('invalid_cells')) > 0:
                raise serializers.ValidationError({
                    'message': 'Khoảng thời gian thuê không hợp lệ'
                })
        except Cell.DoesNotExist:
            raise serializers.ValidationError({
                'message': 'Không tìm thấy ô tủ!'
            })
        return data

