from rest_framework import serializers
from cabinet.models import CampaignCabinet


class CampaignCabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCabinet
        fields = ['campaign_id', 'cabinet_id', 'description']
