from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import AdministrativeRegion
from location.web_api.serializers.administrative_region_serializer import AdministrativeRegionSerializer


@api_view(['GET'])
def get_administrative_region(request):
    """
        Get all administrative_region
        """
    administrative_region = []
    try:
        administrative_region = AdministrativeRegion.objects.all()
    except AdministrativeRegion.DoesNotExist:
        pass

    data = AdministrativeRegionSerializer(administrative_region, many=True).data

    return Response({
        'success': True,
        'data': data,
    })