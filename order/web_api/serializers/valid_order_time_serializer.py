from datetime import timedelta

from dateutil import parser
from django.utils import timezone as tz
from rest_framework import serializers

from cabinet.models import CampaignCabinet, CostVersion, Cabinet
from exe201_backend.common.constants import SystemConstants
from exe201_backend.common.utils import Utils


class ValidOrderTimeRequestSerializer(serializers.Serializer):
    hash_code = serializers.CharField()
    time_start = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    time_end = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def validate(self, data):
        time_start = data['time_start']
        time_end = data['time_end']
        if time_start < tz.now():
            raise serializers.ValidationError({'errorMessage': 'Thời gian bắt đầu phải lớn hơn thời gian hiện tại'})
        if time_start + timedelta(minutes=30) >= time_end:
            raise serializers.ValidationError({'errorMessage': 'Khoảng thời gian không hợp lệ'})
        return data


class ValidOrderSerializer(serializers.Serializer):
    hash_code = serializers.CharField()
    location_detail = serializers.SerializerMethodField()
    depth = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()
    total_cost = serializers.SerializerMethodField()

    def get_total_cost(self, data):
        t_zone = SystemConstants.timezone
        order_time_start = t_zone.localize(parser.parse(data['time_start']))
        order_time_end = t_zone.localize(parser.parse(data['time_end']))
        total_cost = 0
        try:
            campaign_cabinets = (CampaignCabinet.objects.filter(cabinet__id=data['cabinet_id'])
                                                        .select_related('campaign').order_by('campaign__time_start'))
            if not campaign_cabinets:
                raise CampaignCabinet.DoesNotExist
            campaign_cabinets = [campaign_cabinet.campaign for campaign_cabinet in campaign_cabinets]
            # check valid time condition
            # (order_time_start <= campaign_time_end) and (campaign_time_start<= order_time_end)
            valid_campaign_list = [campaign for campaign in campaign_cabinets
                                   if order_time_start <= campaign.time_end and campaign.time_start <= order_time_end]
            for valid_campaign in valid_campaign_list:
                total_cost += Utils.calc_total_cost(valid_campaign, order_time_start, order_time_end)
        except (CampaignCabinet.DoesNotExist, CostVersion.DoesNotExist):
            pass
        return total_cost

    def get_location_detail(self, data):
        location_detail = ''
        try:
            cabinet = Cabinet.objects.get(id=data.get('cabinet_id'),
                                          status=True)
            location_detail = cabinet.controller.location.location_detail
        except Cabinet.DoesNotExist:
            pass
        return location_detail
