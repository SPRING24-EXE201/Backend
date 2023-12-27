from rest_framework import serializers
from cabinet.models import CampaignCabinet


class CampaignCabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCabinet
        fields = ['id', 'campaign_id', 'cabinet_id', 'status']
