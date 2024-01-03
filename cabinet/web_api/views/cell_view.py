from rest_framework.decorators import api_view
from rest_framework.response import Response

from cabinet.models import Cell
from cabinet.web_api.serializers.cell_serializer import CellSerializer


@api_view(['GET'])
def get_cell(request):
    """
    Get all cell
    """
    cell = []
    try:
        cell = Cell.objects.all().filter(status=True)
    except Cell.DoesNotExist:
        pass

    data = CellSerializer(cell, many=True).data

    return Response({
        'success': True,
        'data': data,
    })