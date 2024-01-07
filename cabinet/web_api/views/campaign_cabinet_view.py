from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import CampaignCabinet
from cabinet.web_api.serializers.campaign_cabinet_serializer import CampaignCabinetSerializer


@api_view(['GET'])
def get_campaign_cabinet(self):
    """
    Get all campaign cabinet
    """
    campaign_cabinet = []
    try:
        campaign_cabinet = CampaignCabinet.objects.all()
    except CampaignCabinet.DoesNotExist:
        pass

    data = CampaignCabinetSerializer(campaign_cabinet, many=True).data

    return Response({
        'success': True,
        'data': data,
    })
