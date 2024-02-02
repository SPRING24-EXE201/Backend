from rest_framework.decorators import api_view
from rest_framework.response import Response
from cabinet.models import Cell
from cabinet.web_api.serializers.cell_serializer import CellSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse
@extend_schema(
    parameters=[
        OpenApiParameter(name='cell_id', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.PATH)

    ]
)
@api_view(['GET'])
def get_cell(request, cell_id):
    """
    Get all cell
    """

    try:
        cell = Cell.objects.get(id=cell_id, status = True)
        data = CellSerializer(cell, many=False).data
        status_code = 200
    except Cell.DoesNotExist:
        data = {'message': "Ô tủ không tồn tại"}
        status_code = 400
    finally:
        return JsonResponse(data, status=status_code)



