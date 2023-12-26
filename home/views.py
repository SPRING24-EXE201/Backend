from django.shortcuts import render
from home.models import User, CostVersion, Campaign, CampaignCabinet, District, Location, Ward
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from home.serializer import CostVersionSerializer, CampaignSerializer, CampaignCabinetSerializer, DistrictSerializer, LocationSerializer, WardSerializer


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


@api_view(['GET'])
def get_campaign_cabinet(request):
    campaign_cabinet_list = []
    try:
        campaign_cabinet_list = CampaignCabinet.objects.all()
    except CampaignCabinet.DoesNotExist:
        pass

    data = CampaignCabinetSerializer(campaign_cabinet_list, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@api_view(['GET'])
def get_district(request):
    district_list = []
    try:
        district_list = District.objects.all()
    except DistrictSerializer.DoesNotExist:
        pass
    
    data = DistrictSerializer(district_list, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@api_view(['GET'])
def get_ward(request):
    ward_list = []
    try:
        ward_list = Ward.objects.all()
    except WardSerializer.DoesNotExist:
        pass
    
    data = WardSerializer(ward_list, many=True).data

    return Response({
        'success': True,
        'data': data,
    })


@api_view(['GET'])
def get_location(request):
    location_list = []
    try:
        location_list = Location.objects.all()
    except LocationSerializer.DoesNotExist:
        pass
    
    data = LocationSerializer(location_list, many=True).data

    return Response({
        'success': True,
        'data': data,
    })