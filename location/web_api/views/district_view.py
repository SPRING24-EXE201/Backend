from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import District
from location.web_api.serializers.district_serializer import DistrictSerializer


@api_view(['GET'])
def get_district(request):
    """
    Get all district
    """
    district = []
    try:
        district = District.objects.all()
    except District.DoesNotExist:
        pass

    data = DistrictSerializer(district, many=True).data

    return Response({
        'success': True,
        'data': data,
    })