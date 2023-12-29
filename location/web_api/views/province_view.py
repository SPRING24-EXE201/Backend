from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import Province
from location.web_api.serializers.province_serializer import ProvinceSerializer


@api_view(['GET'])
def get_province(request):
    items = Province.objects.all()
    serializer = ProvinceSerializer(items, many=True)
    return Response(serializer.data)