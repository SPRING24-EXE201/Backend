from rest_framework import serializers

from cabinet.models import CostVersion

class CostVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostVersion
        fields = ['id', 'version', 'from_hour', 'to_hour', 'cost', 'unit', 'status']