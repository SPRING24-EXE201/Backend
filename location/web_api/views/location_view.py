from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from django.db.models import Q, CharField
from django.db.models.functions import Greatest, Lower
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from exe201_backend.common.pagination import CustomPageNumberPagination
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
        OpenApiParameter(name='page_size', required=False, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='page', required=False, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cabinet_location(request, *args, **kwargs):
    """
    List all cabinets follow location.
    """
    CharField.register_lookup(Lower)
    queryset = []
    try:
        queryset = Location.objects.all().order_by('id')
    except Location.DoesNotExist:
        pass
    search_query = request.GET.get('search_query')
    if search_query:
        queryset = queryset.filter(
            Q(ward__name__unaccent__lower__icontains=search_query) |
            Q(location_detail__unaccent__lower__icontains=search_query) |
            Q(ward__district__name__unaccent__lower__icontains=search_query) |
            Q(ward__district__province__name__unaccent__lower__icontains=search_query) |
            Q(location_name__unaccent__lower__icontains=search_query)
        )
    if queryset:
        serializer = CabinetLocationSerializer(queryset, many=True)
        response_data = [location for location in serializer.data if location['cabinets'] is not None]
        if response_data:
            pagination_class = CustomPageNumberPagination
            paginator = pagination_class()
            paginated_response = paginator.paginate_queryset(response_data, request)
            return paginator.get_paginated_response(paginated_response)
    return Response(status=404, data={
        'message': 'Không tìm thấy tủ phù hợp'
    })
