from rest_framework import serializers

from order.models import OrderDetail


class OrderSerializer(serializers.ModelSerializer):
    order_detail_id = serializers.IntegerField(source='id')
    cell_index = serializers.IntegerField(source='cell.cell_index')
    cabinet_description = serializers.CharField(source='cell.cabinet.description')
    location_detail = serializers.CharField(source='cell.cabinet.controller.location.location_detail')
    order_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='order.order_date')
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='time_start')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='time_end')

    class Meta:
        model = OrderDetail
        fields = [
            'order_id',
            'order_detail_id',
            'cell_id',
            'cabinet_description',
            'location_detail',
            'cell_index',
            'order_date',
            'start_date',
            'end_date',
        ]
