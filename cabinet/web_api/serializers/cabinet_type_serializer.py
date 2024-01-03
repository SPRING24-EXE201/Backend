from rest_framework import serializers
from cabinet.models import CabinetType


class CabinetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinetType
        fields = ['type', 'description', 'status', 'image_link', 'cost_per_unit']
