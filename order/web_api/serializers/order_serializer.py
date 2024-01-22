from rest_framework import serializers
from order.models import Order
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
        fields = ['order_id', 'id', 'cell_id', 'cell_index', 'cabinet_description', 'location_detail', 'time_start', 'time_end']

class OrderByUserSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='id')
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
        return obj.orderdetail_set.first().id

    def get_cell_id(self, obj):
        return obj.orderdetail_set.first().cell.id

    def get_cell_index(self, obj):
        return obj.orderdetail_set.first().cell.cell_index

    def get_cabinet_description(self, obj):
        return obj.orderdetail_set.first().cell.cabinet.description

    def get_location_detail(self, obj):
        return obj.orderdetail_set.first().cell.cabinet.controller.location.location_detail

    def get_start_date(self, obj):
        return obj.orderdetail_set.first().time_start

    def get_end_date(self, obj):
        return obj.orderdetail_set.first().time_end
