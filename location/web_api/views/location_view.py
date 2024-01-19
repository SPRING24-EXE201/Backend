from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from exe201_backend.common.pagination import CustomPageNumberPagination
from django.db.models import Q

from location.models import Location
from location.web_api.serializers.location_serializer import LocationSerializer, CabinetLocationSerializer


@api_view(['GET'])
def get_location(request):
    """
    Get all location
    """
    location = []
    try:
        location = Location.objects.all()
    except Location.DoesNotExist:
        pass

    data = LocationSerializer(location, many=True).data

    return Response({
        'success': True,
        'data': data,
    })


@extend_schema(
    parameters=[
        OpenApiParameter(name='search_query', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='page_size', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='page', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cabinet_location(request, *args, **kwargs):
    """
    List all cabinets follow location.
    """
    queryset = []
    try:
        queryset = Location.objects.all().order_by('id')
    except Location.DoesNotExist:
        pass
    search_query = request.GET.get('search_query')
    page = request.GET.get('page')
    page_size = request.GET.get('page_size')
    if search_query is not None:
        queryset = queryset.filter(
            Q(ward_id__name__icontains=search_query) |
            Q(location_detail__icontains=search_query) |
            Q(ward_id__district_id__name__icontains=search_query) |
            Q(ward_id__district_id__province_id__name__icontains=search_query)
        )
    if len(queryset) > 0:
        pagination_class = CustomPageNumberPagination
        paginator = pagination_class()
        paginator.page_size = int(page_size)
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        if paginated_queryset is not None:
            serializer = CabinetLocationSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
    return Response(status=404, data={
                    'message': 'Không tìm thấy tủ phù hợp'
                    })
