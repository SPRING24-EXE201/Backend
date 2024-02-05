from rest_framework import serializers

from exe201_backend.common.payment_method_enum import PaymentMethod
from order.models import Order
from order.models import OrderDetail


class OrderCellRequestSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
    cell_id = serializers.IntegerField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    is_desc = serializers.BooleanField(required=False, default=False)
    is_rented = serializers.BooleanField(required=False, default=True)
    is_renting = serializers.BooleanField(required=False, default=True)
    is_ordered = serializers.BooleanField(required=False, default=True)

    def validate(self, data):
        time_start = data.get('start_date')
        time_end = data.get('end_date')
        if time_start is None or time_end is None:
            return data
        is_valid_range = time_start <= time_end
        if not is_valid_range:
            raise serializers.ValidationError({
                'message': 'Khoảng thời gian không hợp lệ'
            })
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_detail_id = serializers.IntegerField(source='id')
    cell_index = serializers.IntegerField(source='cell.cell_index')
    cabinet_description = serializers.CharField(source='cell.cabinet.description')
    location_detail = serializers.CharField(source='cell.cabinet.controller.location.location_detail')
    order_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='order.order_date')
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='time_start')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='time_end')

    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'payment_method', 'order_date', 'status']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='order.id', read_only=True)
    cell_id = serializers.CharField(source='cell.id', read_only=True)
    cell_index = serializers.CharField(source='cell.cell_index', read_only=True)
    cabinet_description = serializers.CharField(source='cell.cabinet.description', read_only=True)
    location_detail = serializers.CharField(source='cell.cabinet.controller.location.location_detail', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ['order_id', 'id', 'cell_id', 'cell_index', 'cabinet_description', 'location_detail', 'time_start',
                  'time_end']


class OrderByUserSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='order.id')
    order_detail_id = serializers.IntegerField(source='id')
    cell_id = serializers.IntegerField(source='cell.id')
    cell_index = serializers.IntegerField(source='cell.cell_index')
    cabinet_description = serializers.CharField(source='cell.cabinet.description')
    location_detail = serializers.CharField(source='cell.cabinet.controller.location.location_detail')
    order_date = serializers.DateTimeField(source='order.order_date')
    start_date = serializers.DateTimeField(source='time_start')
    end_date = serializers.DateTimeField(source='time_end')
    height = serializers.FloatField(source='cell.height')
    width = serializers.FloatField(source='cell.width')
    depth = serializers.FloatField(source='cell.depth')
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = ['order_id', 'order_detail_id', 'cell_id', 'cell_index', 'cabinet_description', 'location_detail',
                  'order_date', 'start_date', 'end_date', 'height', 'width', 'depth', 'payment_method']

    def get_payment_method(self, obj):
        try:
            return PaymentMethod(obj.order.payment_method).name
        except ValueError:
            return ''
