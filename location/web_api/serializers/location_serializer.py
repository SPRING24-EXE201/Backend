from django.db.models import Q
from rest_framework import serializers

from location.models import Location
from cabinet.models import Cabinet, Cell, Controller
from django.utils import timezone


class CabinetSerializer(serializers.ModelSerializer):
    empty_cells = serializers.SerializerMethodField()
    cabinet_id = serializers.IntegerField(source='id')

    class Meta:
        model = Cabinet
        fields = ['cabinet_id', 'description', 'empty_cells']

    def get_empty_cells(self, obj):
        now = timezone.now()

        # Case 1: user_id is null and expired_date is null
        query_user_not_exists = Q(cabinet_id=obj.id,
                                  user_id__isnull=True,
                                  expired_date__isnull=True
                                  )

        # Case 2: user_id is not null and expired_date is less than or equal to now
        query_user_exists = Q(cabinet_id=obj.id,
                              expired_date__isnull=False,
                              expired_date__lte=now,
                              user_id__isnull=False
                              )

        return Cell.objects.filter(query_user_exists | query_user_not_exists).count()

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

class CabinetLocationSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(source='id')
    ward_name = serializers.CharField(source='ward_id.name')
    district_name = serializers.CharField(source='ward_id.district_id.name')
    province_name = serializers.CharField(source='ward_id.district_id.province_id.name')
    cabinets = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['location_id', 'ward_name', 'district_name', 'province_name', 'location_detail', 'location_name',
                  'cabinets']

    def get_cabinets(self, obj):
        cabinets = Cabinet.objects.filter(controller_id__location_id__id=obj.id)
        return CabinetSerializer(cabinets, many=True).data
