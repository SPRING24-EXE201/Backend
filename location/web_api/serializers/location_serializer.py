from rest_framework import serializers

from location.models import Location
from cabinet.models import Cabinet, Cell, Controller
from django.utils import timezone


class CabinetSerializer(serializers.ModelSerializer):
    empty_cells = serializers.SerializerMethodField()
    cabinet_id = serializers.IntegerField(source='id')
    description = serializers.CharField()

    class Meta:
        model = Cabinet
        fields = ['cabinet_id', 'description', 'empty_cells']

    def get_empty_cells(self, obj):
        now = timezone.now()
        empty_cells = 0
        all_cells = Cell.objects.filter(cabinet_id=obj.id)
        for cell in all_cells:
            if cell.expired_date < now or cell.user_id is None:
                empty_cells += 1
        return empty_cells
    
    def get_description(self, obj):
        return obj.description

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

class CabinetLocationSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(source='id')
    location_name = serializers.CharField()
    ward_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    cabinets = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['location_id', 'ward_name', 'district_name', 'province_name', 'location_detail', 'location_name',
                  'cabinets']

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
