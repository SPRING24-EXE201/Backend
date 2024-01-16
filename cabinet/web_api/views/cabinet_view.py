from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404

from cabinet.models import Cabinet
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer, CabinetDetailsSerializer


@api_view(['GET'])
def get_cabinet(request):
    """
    Get all cabinet
    """
    cabinet = []
    try:
        cabinet = Cabinet.objects.all().filter(status=True)
    except Cabinet.DoesNotExist:
        pass

    data = CabinetDetailsSerializer(cabinet, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@api_view(['GET'])
def get_cabinet_by_id(request, cabinet_id):
    """
    Get cabinet by id
    """
    cabinet = []
    try:
        cabinet = Cabinet.objects.get(id=cabinet_id)
    except Cabinet.DoesNotExist:
        raise Http404("Not found")

    data = CabinetDetailsSerializer(cabinet).data

    return Response({
        'success': True,
        'data': data,
    })