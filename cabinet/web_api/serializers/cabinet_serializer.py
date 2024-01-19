from rest_framework import serializers
from cabinet.models import Cabinet, Cell
from order.models import OrderDetail
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'controller_id', 'cabinetType_id', 'description', 'start_using_date', 'height', 'width',
                  'depth', 'status', 'image_link', 'virtual_cabinet_id']


class CabinetDetailsSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='controller_id.location_id.location_name', read_only=True)
    location_detail = serializers.CharField(source='controller_id.location_id.location_detail', read_only=True)
    empty_cell = serializers.SerializerMethodField(method_name='get_empty_cells')
    cabinet_type = serializers.CharField(source='cabinetType_id.type', read_only=True)

    class Meta:
        model = Cabinet
        fields = ['location_name', 'location_detail', 'width', 'height', 'depth', 'empty_cell', 'cabinet_type']

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

        