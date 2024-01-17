from rest_framework import serializers
from home.models import User, CostVersion, Campaign, CampaignCabinet, Location, Ward, District


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

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['province_id', 'administrative_unit_id', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name']


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['district_id', 'administrative_unit_id', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'ward_id', 'location_detail']
