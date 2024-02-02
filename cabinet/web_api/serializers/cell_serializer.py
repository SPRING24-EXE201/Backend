from rest_framework import serializers

from cabinet.models import Cell


class CellSerializer(serializers.ModelSerializer):
    cabinet_description = serializers.SerializerMethodField()
    location_detail = serializers.SerializerMethodField()
    class Meta:
        model = Cell
        fields = ['id', 'cell_index', 'height', 'width', 'depth', 'cabinet_description', 'location_detail']

    def get_cabinet_description(self, obj):
        return obj.cabinet.description if obj.cabinet else None
    def get_location_detail(self, obj):
        return obj.cabinet.controller.location.location_detail if obj.cabinet.controller.location else None