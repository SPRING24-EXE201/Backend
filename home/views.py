from django.shortcuts import render
from home.models import User, CostVersion, Campaign
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from home.serializer import CostVersionSerializer, CampaignSerializer

@api_view(['GET'])
def get_cost_version(request):
    """
    Get cost version
    :param request:
    :return:
    """
    cost_version = []
    try:
        cost_version = CostVersion.objects.all().filter(status=True)
    except CostVersion.DoesNotExist:
        pass

    data = CostVersionSerializer(cost_version, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@api_view(['GET'])
def get_campaign(request):
    campaign_list = []
    try:
        campaign_list = Campaign.objects.all().filter(status=True)
    except Campaign.DoesNotExist:
        pass

    data = CampaignSerializer(campaign_list, many=True).data

    return Response({
        'success': True,
        'data': data,
    })