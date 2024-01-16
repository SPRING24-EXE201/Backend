from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import CostVersion
from cabinet.web_api.serializers.cost_version_serializer import CostVersionSerializer


@api_view(['GET'])
def get_cost_version(request):
    """
    Get all cost version
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