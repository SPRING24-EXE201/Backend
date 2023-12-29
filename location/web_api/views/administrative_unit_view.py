from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import AdministrativeUnit
from location.web_api.serializers.administrative_unit_serializer import AdministrativeUnitSerializer


@api_view(['GET'])
def get_administrative_unit(request):
    items = AdministrativeUnit.objects.all()
    serializer = AdministrativeUnitSerializer(items, many=True)
    return Response(serializer.data)