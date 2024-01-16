from rest_framework import serializers
from cabinet.models import Cabinet, Cell
from order.models import OrderDetail
from datetime import datetime, timedelta
from django.utils import timezone


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'controller_id', 'cabinetType_id', 'description', 'start_using_date', 'height', 'width',
                  'depth', 'status', 'image_link', 'virtual_cabinet_id']


class CabinetDetailsSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='controller_id.location_id.location_name', read_only=True)
    location_detail = serializers.CharField(source='controller_id.location_id.location_detail', read_only=True)
    empty_cell = serializers.SerializerMethodField(method_name='get_empty_cell')
    cabinet_type = serializers.CharField(source='cabinetType_id.type', read_only=True)

    class Meta:
        model = Cabinet
        fields = ['location_name', 'location_detail', 'width', 'height', 'depth', 'empty_cell', 'cabinet_type']

    def get_empty_cell(self, obj):
        now = timezone.now()
        empty_cells = 0
        all_cells = Cell.objects.filter(cabinet_id=obj.id)
        for cell in all_cells:
            if cell.expired_date < now or cell.user_id is None:
                empty_cells += 1
        return empty_cells

        