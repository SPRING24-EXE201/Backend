from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import CabinetType
from cabinet.web_api.serializers.cabinet_type_serializer import CabinetTypeSerializer


@api_view(['GET'])
def get_cabinet_type(request):
    """
    Get all cabinet type
    """
    cabinet_type = []
    try:
        cabinet_type = CabinetType.objects.all().filter(status=True)
    except CabinetType.DoesNotExist:
        pass

    data = CabinetTypeSerializer(cabinet_type, many=True).data

    return Response({
        'success': True,
        'data': data,
    })