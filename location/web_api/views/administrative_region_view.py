from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import AdministrativeRegion
from location.web_api.serializers.administrative_region_serializer import AdministrativeRegionSerializer


@api_view(['GET'])
def get_administrative_region(request):
    items = AdministrativeRegion.objects.all()
    serializer = AdministrativeRegionSerializer(items, many=True)
    return Response(serializer.data)