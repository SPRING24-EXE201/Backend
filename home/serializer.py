from rest_framework import serializers
from home.models import User, CostVersion, Campaign, CampaignCabinet


class CostVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostVersion
        fields = "__all__"


class CampaignSerializer(serializers.ModelSerializer):
    cost_version_id = CostVersionSerializer()

    class Meta:
        model = Campaign
        fields = ['id', 'time_start', 'time_end', 'cost_version_id', 'status']


class CampaignCabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCabinet
        fields = ['campaign_id', 'cabinet_id', 'description']
