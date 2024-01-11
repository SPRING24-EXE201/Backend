from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import Cabinet
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer


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

    data = CabinetSerializer(cabinet, many=True).data

    return Response({
        'success': True,
        'data': data,
    })