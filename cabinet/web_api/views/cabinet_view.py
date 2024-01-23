from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from exe201_backend.common import utils
from cabinet.models import Cabinet, Cell
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer, EmptyCellsSerializer, \
    EmptyCellsRequestSerializer, CabinetNearbySerializer
from location.models import Location, Ward, District, Province
from order.models import OrderDetail
from exe201_backend.common.pagination import CustomPageNumberPagination
from django.http import JsonResponse

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
        not_empty_cells = OrderDetail.objects.filter(time_end__gte=needed_time_start,
                                                     time_start__lte=needed_time_end,
                                                     order__status=True)
        # get cell_id of not empty cells
        not_empty_cells = not_empty_cells.values_list('cell__id', flat=True).distinct()
        empty_cells = Cell.objects.filter(cabinet__id=cabinet_id,
                                          cabinet__status=True,
                                          status__gt=0).exclude(id__in=not_empty_cells)

    empty_cells_data = EmptyCellsSerializer(empty_cells, many=True).data

    return Response({
        'columns': cabinet.column_number,
        'rows': cabinet.row_number,
        'empty_cells': empty_cells_data
    })

def distance(l1, a1, l2, a2):
    return float(((l2 - l1) ** 2 + (a2 - a1) ** 2) ** 0.5)

@extend_schema(
    parameters=[
        OpenApiParameter(name='longitude', required=True, type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='latitude', required=True, type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='page_size', required=False, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='page', required=False, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),
    ]
)
@api_view(['GET'])
def get_cabinet_nearby(request):
    try:
        longitude = float(request.GET.get('longitude'))
        latitude = float(request.GET.get('latitude'))
        queryset_locations = Location.objects.all()
        locations = list(queryset_locations)
        locations = sorted(locations, key= lambda l: distance(longitude, latitude, l.longitude, l.latitude))
        data = []
        for location in locations:
            cabinets = Cabinet.objects.select_related('controller__location').filter(controller__location__id= location.id)
            for cabinet in cabinets:
                cells = Cell.objects.filter(cabinet_id = cabinet.id).values('id')
                empty_cells = utils.Utils.get_empty_cells_by_order_details(cells)

                location_empty_cell = {"location_detail" : location.location_detail,
                                        "ward_name" : location.ward.name,
                                        "cabinet_id" : cabinet.id,
                                        "cabinet_name": cabinet.name,
                                        "district_name" : location.ward.district.name,
                                        "province_name" : location.ward.district.province.name,
                                        "empty_cell" : empty_cells}

                data.append(location_empty_cell)

        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(data, request)
        serializer = CabinetNearbySerializer(result_page, many=True)

        data = serializer.data
        status_code = 200

    except Exception as e:
        data = str(e)
        status_code = 500
    finally:
        return JsonResponse(data, status = status_code, safe = False)


