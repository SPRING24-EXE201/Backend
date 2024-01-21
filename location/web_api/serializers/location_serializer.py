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
        now = timezone.now()
        empty_cell_num = 0
        # Case 1: user_id is null and expired_date is null
        empty_cell_num += Cell.objects.filter(cabinet__id=obj.id,
                                              user_id__isnull=True,
                                              expired_date__isnull=True,
                                              status__gt=0
                                              ).count()

        # Case 2: user_id is not null and expired_date is less than or equal to now
        cell_user_exists = Cell.objects.filter(cabinet__id=obj.id,
                                               expired_date__isnull=False,
                                               expired_date__lte=now,
                                               user_id__isnull=False,
                                               status__gt=0
                                               ).values_list('id', flat=True)
        if cell_user_exists:
            order_details = (OrderDetail.objects.filter(cell__id__in=cell_user_exists)
                                                .values('cell', 'user', 'time_start', 'time_end'))
            if order_details:
                empty_cell_num += Utils.get_empty_cells_by_order_details(order_details=order_details,
                                                                         cell_id_list=cell_user_exists)
            else:
                empty_cell_num += len(cell_user_exists)
        return empty_cell_num

    
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
        return CabinetSerializer(cabinets, many=True).data
