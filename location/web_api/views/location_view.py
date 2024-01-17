from rest_framework.decorators import api_view
from rest_framework.response import Response
from location.utils.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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


@api_view(['GET'])
def get_cabinet_location(request, pageSize, page, search_query):
    """
    List all cabinets follow location.
    """
    try:
        queryset = Location.objects.all().order_by('id')

        filter_backends = [DjangoFilterBackend, filters.SearchFilter]

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(request, queryset, get_cabinet_location)

        if search_query:
            queryset = queryset.filter(
                Q(ward_id__name__icontains=search_query) |
                Q(location_detail__icontains=search_query) |
                Q(ward_id__district_id__name__icontains=search_query) |
                Q(ward_id__district_id__province_id__name__icontains=search_query)
            )

        pagination_class = CustomPageNumberPagination
        paginator = pagination_class()
        paginator.page_size = int(pageSize)
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        if paginated_queryset is not None:
            serializer = CabinetLocationSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CabinetLocationSerializer(queryset, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'status': False,
            'message': str(e)
        })
