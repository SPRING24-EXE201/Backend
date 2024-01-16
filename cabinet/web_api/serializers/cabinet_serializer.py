from rest_framework import serializers
from cabinet.models import Cabinet, Cell
from order.models import OrderDetail
from datetime import datetime, timedelta


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'controller_id', 'cabinetType_id', 'description', 'start_using_date', 'height', 'width',
                  'depth', 'status', 'image_link', 'virtual_cabinet_id']


class CabinetDetailsSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='controller_id.location_id.location_name', read_only=True)
    location_detail = serializers.CharField(source='controller_id.location_id.location_detail', read_only=True)
    empty_cell = serializers.SerializerMethodField()
    cabinet_type = serializers.CharField(source='cabinetType_id.type', read_only=True)

    class Meta:
        model = Cabinet
        fields = ['location_name', 'location_detail', 'width', 'height', 'depth', 'empty_cell', 'cabinet_type']

    def get_empty_cell(self, obj):
        now = datetime.now()
        count_user_is_null = Cell.objects.filter(cabinet_id=obj.id, user_id__isnull=True).count()
        cells = OrderDetail.objects.extra(where=["time_start >= %s OR time_end <= %s"],
                                          params=[now + timedelta(minutes=30), now]).count()
        empty_cells_count = count_user_is_null + cells
        return empty_cells_count
        