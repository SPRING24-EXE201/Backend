from rest_framework import serializers

from cabinet.models import CellLog


class CellLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellLog
        fields = '__all__'
