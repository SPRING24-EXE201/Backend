from rest_framework.decorators import api_view
from rest_framework.response import Response

from location.models import AdministrativeUnit
from location.web_api.serializers.administrative_unit_serializer import AdministrativeUnitSerializer


@api_view(['GET'])
def get_administrative_unit(request):
    """
        Get all administrative_unit
        """
    administrative_unit = []
    try:
        administrative_unit = AdministrativeUnit.objects.all()
    except AdministrativeUnit.DoesNotExist:
        pass

    data = AdministrativeUnitSerializer(administrative_unit, many=True).data

    return Response({
        'success': True,
        'data': data,
    })