from rest_framework import serializers
from cabinet.models import CampaignCabinet


class CampaignCabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCabinet
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 'cost_versions']
