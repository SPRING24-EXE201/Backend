from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import Province
from location.web_api.serializers.province_serializer import ProvinceSerializer


@api_view(['GET'])
def get_province(request):
    """
        Get all province
        """
    province = []
    try:
        province = Province.objects.all()
    except Province.DoesNotExist:
        pass

    data = ProvinceSerializer(province, many=True).data

    return Response({
        'success': True,
        'data': data,
    })