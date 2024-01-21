from django.utils import timezone
from rest_framework import serializers

from cabinet.models import Cabinet, Cell
from exe201_backend.common.utils import Utils
from location.models import Location
from order.models import OrderDetail


class CabinetSerializer(serializers.ModelSerializer):
    empty_cells = serializers.SerializerMethodField()
    cabinet_id = serializers.IntegerField(source='id')

    class Meta:
        model = Cabinet
        fields = ['cabinet_id', 'description', 'empty_cells']

    def get_empty_cells(self, obj):
        cabinet_cells = Cell.objects.filter(cabinet__id=obj.id,
                                            status__gt=0
                                            ).values_list('id', flat=True)
        return Utils.get_empty_cells_by_order_details(cabinet_cells)

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

class CabinetLocationSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(source='id')
    ward_name = serializers.CharField(source='ward.name')
    district_name = serializers.CharField(source='ward.district.name')
    province_name = serializers.CharField(source='ward.district.province.name')
    cabinets = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['location_id', 'ward_name', 'district_name', 'province_name', 'location_detail', 'location_name',
                  'cabinets']

    def get_cabinets(self, obj):
        cabinets = Cabinet.objects.filter(controller__location__id=obj.id, status=True)
        if not cabinets:
            return None
        return CabinetSerializer(cabinets, many=True).data
