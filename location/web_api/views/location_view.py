from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import Location
from location.web_api.serializers.location_serializer import LocationSerializer


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