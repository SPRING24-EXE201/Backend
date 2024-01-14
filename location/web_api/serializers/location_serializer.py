from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from location.models import Location, Ward, District, Province
from cabinet.models import Cabinet, Controller, Cell
from order.models import Order, OrderDetail
from datetime import datetime, timedelta
from django.db.models import Count, Q
import django_filters.rest_framework


class CabinetSerializer(serializers.ModelSerializer):
    empty_cells = serializers.SerializerMethodField(method_name='get_empty_cells_count')
    cabinet_id = serializers.IntegerField(source='id')
    description = serializers.SerializerMethodField()

    class Meta:
        model = Cabinet
        fields = ['cabinet_id', 'empty_cells', 'description']

    def get_empty_cells_count(self, obj):
        now = datetime.now()
        count_user_is_null = Cell.objects.filter(cabinet_id=obj.id, user_id__isnull=True).count()
        cells = OrderDetail.objects.extra(where=["time_start >= %s OR time_end <= %s"],
                                          params=[now + timedelta(minutes=30), now]).count()
        empty_cells_count = count_user_is_null + cells
        return empty_cells_count
    
    def get_description(self, obj):
        return obj.description

class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controller
        fields = ['id', 'location_id']

class LocationSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(source='id')
    location_name = serializers.CharField()
    ward_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    cabinets = serializers.SerializerMethodField()
    #controllers = ControllerSerializer(source='controller_set', many=True, read_only=True)
    

    class Meta:
        model = Location
        fields = ['location_id', 'ward_name', 'district_name', 'province_name', 'location_detail', 'location_name', 'cabinets']

    def get_ward_name(self, obj):
        return obj.ward_id.name
    
    def get_district_name(self, obj):
        return obj.ward_id.district_id.name
    
    def get_province_name(self, obj):
        return obj.ward_id.district_id.province_id.name

    def get_description(self, obj):
        return obj.description
    
    def get_cabinets(self, obj):
        controllers = Controller.objects.filter(location_id=obj.id)
        cabinets = Cabinet.objects.filter(controller_id__in=controllers.values_list('id', flat=True))
        return CabinetSerializer(cabinets, many=True).data
    
    
    
