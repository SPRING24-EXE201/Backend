from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from jsonschema.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from cabinet.models import Cabinet, Cell
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer, EmptyCellsSerializer, EmptyCellsRequestSerializer, CabinetDetailsSerializer
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

    data = CabinetDetailsSerializer(cabinet, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@extend_schema(
    parameters=[
        OpenApiParameter(name='cabinet_id', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),        
    ]
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cabinet_by_id(request, *args):
    """
    Get cabinet by id
    """
    queryset = []
    try:
        queryset = Cabinet.objects.all().filter(id=request.GET.get('cabinet_id'))                    
    except Cabinet.DoesNotExist:
        pass
    except Exception as e:
        pass
    finally:
        data = CabinetDetailsSerializer(queryset, many=True).data  
        return Response(data)

@extend_schema(
    parameters=[
        OpenApiParameter(name='cabinet_id', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.PATH),
        OpenApiParameter(name='time_start', required=True, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='time_end', required=True, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_empty_cells(request, cabinet_id):
    """
    Get all empty cells of a specified cabinet
    """
    request.query_params.appendlist('cabinet_id', cabinet_id)
    serializer = EmptyCellsRequestSerializer(data=request.query_params)
    empty_cells = []
    if serializer.is_valid(raise_exception=True):
        needed_time_start = serializer.data.get('time_start')
        needed_time_end = serializer.data.get('time_end')
        cabinet_id = serializer.data.get('cabinet_id')
        try:
            # not empty cells condition:
            # (needed_time_start <= order_detail_time_end) and (order_detail_time_start<= needed_time_end)
            not_empty_cells = OrderDetail.objects.filter(time_end__gte=needed_time_start,
                                                         time_start__lte=needed_time_end)
            # get cell_id of not empty cells
            not_empty_cells = not_empty_cells.values_list('cell_id__id', flat=True).distinct()
            empty_cells = Cell.objects.filter(cabinet_id__id=cabinet_id,
                                              cabinet_id__status=True,
                                              status__gt=0).exclude(id__in=not_empty_cells)
        except Cell.DoesNotExist:
            pass
        except OrderDetail.DoesNotExist:
            pass

    data = EmptyCellsSerializer(empty_cells, many=True).data
    return Response(data)
