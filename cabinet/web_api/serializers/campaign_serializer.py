from rest_framework import serializers
from cabinet.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 'cost_versions']
