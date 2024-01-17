from rest_framework import serializers
from order.models import Order
from order.models import OrderDetail

class OrderSerializer(serializers.ModelSerializer):
    order_detail_id = serializers.IntegerField(source='id')
    cell_index = serializers.IntegerField(source='cell_id.cell_index')
    cabinet_description = serializers.CharField(source='cell_id.cabinet_id.description')
    location_detail = serializers.CharField(source='cell_id.cabinet_id.controller_id.location_id.location_detail')
    order_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='order_id.order_date')
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='time_start')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='time_end')
    class Meta:
        model = Order
        fields = ['order_id', 'total_amount', 'payment_method', 'order_date', 'status']

class OrderDetailSerializer(serializers.ModelSerializer):
    order_id = serializers.ReadOnlyField(source='order.order_id')
    cell_id = serializers.ReadOnlyField(source='cell_id.id')
    cell_index = serializers.ReadOnlyField(source='cell_id.cell_index')
    cabinet_description = serializers.ReadOnlyField(source='cell_id.cabinet_id.description')
    location_detail = serializers.ReadOnlyField(source='cell_id.cabinet_id.controller_id.location_id.location_detail')

    class Meta:
        model = OrderDetail
        fields = ['order_id', 'id', 'cell_id', 'cell_index', 'cabinet_description', 'location_detail', 'time_start', 'time_end']

class OrderByUserSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='id')
    order_detail_id = serializers.SerializerMethodField()
    cell_id = serializers.SerializerMethodField()
    cell_index = serializers.SerializerMethodField()
    cabinet_description = serializers.SerializerMethodField()
    location_detail = serializers.SerializerMethodField()
    order_date = serializers.DateTimeField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'order_detail_id', 'cell_id', 'cell_index', 'cabinet_description', 'location_detail', 'order_date', 'start_date', 'end_date']

    def get_order_detail_id(self, obj):
        return obj.order_detail.first().id

    def get_cell_id(self, obj):
        return obj.order_detail.first().cell_id.id

    def get_cell_index(self, obj):
        return obj.order_detail.first().cell_id.cell_index

    def get_cabinet_description(self, obj):
        return obj.order_detail.first().cell_id.cabinet_id.description

    def get_location_detail(self, obj):
        return obj.order_detail.first().cell_id.cabinet_id.controller_id.location_id.location_detail

    def get_start_date(self, obj):
        return obj.order_detail.first().time_start

    def get_end_date(self, obj):
        return obj.order_detail.first().time_end
