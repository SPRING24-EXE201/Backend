from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import CellLog
from cabinet.web_api.serializers.cell_log_serializer import CellLogSerializer


@api_view(['GET'])
def get_cell_log(request):
    """
    Get all cell log
    """
    cell_log = []
    try:
        cell_log = CellLog.objects.all()
    except CellLog.DoesNotExist:
        pass

    data = CellLogSerializer(cell_log, many=True).data

    return Response({
        'success': True,
        'data': data,
    })