from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cabinet.models import Cabinet, Cell
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer, EmptyCellsSerializer, \
    EmptyCellsRequestSerializer
from order.models import OrderDetail
from rest_framework.response import Response
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from math import sqrt
from operator import itemgetter
from django.db.models import Count, Q
from cabinet.models import Cabinet
from cabinet.web_api.serializers.cabinet_serializer import CabinetByLocation
from cabinet.pagination import CustomPageNumberPagination


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

def euclidean_distance(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_cabinet_by_location(request):
    try:
        pos_x = request.GET.get('pos_x', None)
        pos_y = request.GET.get('pos_y', None)

        if pos_x is None and pos_y is None:
            cabinets = Cabinet.objects.all().filter(status=True)
        else:
            if pos_x is None or pos_y is None:
                raise Exception('Missing coordinates')

        cabinets = Cabinet.objects.annotate(
            empty_cells=Count('cell', filter=Q(cell__user_id__isnull=True) |
                                             Q(cell__expired_date__lt=timezone.now()))
        ).filter(status=True, empty_cells__gt=0)

        cabinets = Cabinet.objects.filter(status=True)

        if pos_x is not None and pos_y is not None:
            cabinets_distances = []
            for cabinet in cabinets:
                distance = euclidean_distance(float(pos_x), float(pos_y), cabinet.controller.location.longitude, cabinet.controller.location.latitude)
                cabinets_distances.append((cabinet, distance))
                status_code = 200

            # Sort cabinets by distance
            cabinets_distances.sort(key=itemgetter(1))

            # Replace cabinets with sorted list
            cabinets = [cabinet_distance[0] for cabinet_distance in cabinets_distances]

        # Create a pagination instance
        paginator = CustomPageNumberPagination()

        # Get the paginated results
        page_cabinets = paginator.paginate_queryset(cabinets, request)
        serializer = CabinetByLocation(page_cabinets, many=True)

        return paginator.get_paginated_response(serializer.data)
    except Cabinet.DoesNotExist:
        data = {'message': 'Cabinet does not exist'}
        status_code = 404
    finally:
        if 'data' in locals() and 'status_code' in locals():
            return JsonResponse(data, status=status_code, safe=False)


