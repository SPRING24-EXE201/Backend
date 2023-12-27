from rest_framework import serializers
from cabinet.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'cost_version_id', 'time_start', 'time_end', 'status', 'description']
