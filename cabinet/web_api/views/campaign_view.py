from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import Campaign
from cabinet.web_api.serializers.campaign_serializer import CampaignSerializer


@api_view(['GET'])
def get_campaign(request):
    """
    Get all campaign
    """
    campaign = []
    try:
        campaign = Campaign.objects.all().filter(status=True)
    except Campaign.DoesNotExist:
        pass

    data = CampaignSerializer(campaign, many=True).data

    return Response({
        'success': True,
        'data': data,
    })