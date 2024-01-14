from django.db.models import Q
from django.core.paginator import Paginator
from cabinet.models import Cabinet, Controller
from order.models import OrderDetail
from datetime import datetime
from location.models import Location
from location.web_api.serializers.location_serializer import LocationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters, viewsets, pagination
from django_filters.rest_framework import DjangoFilterBackend


class LocationPagination(pagination.PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'page'


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


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['ward_id__name', 'location_detail', 'ward_id__district_id__name',
                     'ward_id__district_id__province_id__name']
    pagination_class = LocationPagination
