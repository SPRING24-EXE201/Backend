from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cabinet.models import Cabinet, Cell
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer, CellStatusSerializer, \
    EmptyCellsRequestSerializer
from order.models import OrderDetail


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


@extend_schema(
    parameters=[
        OpenApiParameter(name='cabinet_id', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.PATH),
        OpenApiParameter(name='time_start', required=True, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='time_end', required=True, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cell_status(request, cabinet_id):
    """f
    Get all empty cells of a specified cabinet
    """
    request.query_params.appendlist('cabinet_id', cabinet_id)
    serializer = EmptyCellsRequestSerializer(data=request.query_params)
    cells = []
    cabinet = None
    try:
        cabinet = Cabinet.objects.get(id=cabinet_id)
    except Cabinet.DoesNotExist:
        raise ValidationError({
            'message': 'Không tìm thấy tủ'
        })
    if serializer.is_valid(raise_exception=True):
        needed_time_start = serializer.data.get('time_start')
        needed_time_end = serializer.data.get('time_end')
        cabinet_id = serializer.data.get('cabinet_id')
        # not empty cells condition:
        # (needed_time_start <= order_detail_time_end) and (order_detail_time_start<= needed_time_end)
        current_orders = OrderDetail.objects.filter(time_end__gte=needed_time_start,
                                                    time_start__lte=needed_time_end,
                                                    order__status=True).select_related('cell')
        # get cell_id of not empty cells
        not_empty_cells_id = current_orders.values_list('cell__id', flat=True).distinct()
        cells_in_cabinet = Cell.objects.filter(cabinet__id=cabinet_id,
                                               cabinet__status=True,
                                               status__gt=0)
        not_empty_cells = [cell for cell in cells_in_cabinet if cell.id in not_empty_cells_id]
        empty_cells = [cell for cell in cells_in_cabinet if cell.id not in not_empty_cells_id]

        empty_cells_data = CellStatusSerializer(empty_cells, many=True).data
        empty_cells_data = [dict(cell, **{'is_empty': True}) for cell in empty_cells_data]
        not_empty_cells_data = CellStatusSerializer(not_empty_cells, many=True).data
        not_empty_cells_data = [dict(cell, **{'is_empty': False}) for cell in not_empty_cells_data]
        cells.extend(not_empty_cells_data)
        cells.extend(empty_cells_data)
        cells.sort(key=lambda cell: cell['cell_index'])
    return Response({
        'columns': cabinet.column_number,
        'rows': cabinet.row_number,
        'cells': cells
    })
