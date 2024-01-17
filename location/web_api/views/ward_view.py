from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import Ward
from location.web_api.serializers.ward_serializer import WardSerializer


@api_view(['GET'])
def get_ward(request):
    """
    Get all ward
    """
    ward = []
    try:
        ward = Ward.objects.all()
    except Ward.DoesNotExist:
        pass

    data = WardSerializer(ward, many=True).data

    return Response({
        'success': True,
        'data': data,
    })