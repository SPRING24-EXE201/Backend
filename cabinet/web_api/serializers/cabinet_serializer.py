from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from cabinet.models import Cabinet, Cell


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'controller_id', 'cabinetType_id', 'description', 'start_using_date', 'height', 'width',
                  'depth', 'status', 'image_link', 'virtual_cabinet_id']


class CabinetDetailsSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='controller.location.location_name', read_only=True)
    location_detail = serializers.CharField(source='controller.location.location_detail', read_only=True)
    empty_cell = serializers.SerializerMethodField(method_name='get_empty_cells')
    cabinet_type = serializers.CharField(source='cabinet_type.type', read_only=True)

    class Meta:
        model = Cabinet
        fields = ['location_name', 'location_detail', 'width', 'height', 'depth', 'empty_cell', 'description', 'cabinet_type']

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

        
class EmptyCellsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ['hash_code', 'cell_index', 'width', 'height', 'depth']


class EmptyCellsRequestSerializer(serializers.Serializer):
    cabinet_id = serializers.IntegerField(required=True)
    time_start = serializers.DateTimeField(required=True)
    time_end = serializers.DateTimeField(required=True)

    def validate(self, data):
        time_start = data['time_start']
        time_end = data['time_end']
        if time_start < timezone.now():
            raise serializers.ValidationError({'errorMessage': 'Thời gian bắt đầu phải lớn hơn thời gian hiện tại'})
        if time_start + timedelta(minutes=30) >= time_end:
            raise serializers.ValidationError({'errorMessage': 'Khoảng thời gian không hợp lệ'})
        return data