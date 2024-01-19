from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from cabinet.models import Cabinet
from cabinet.web_api.serializers.cabinet_serializer import CabinetSerializer, CabinetDetailsSerializer

@api_view(['GET'])
def get_cabinet(request):
    """
    Get all cabinet
    """
    cabinet = []
    try:
        cabinet = Cabinet.objects.all().filter(status=True)
    except Cabinet.DoesNotExist:
        pass

    data = CabinetDetailsSerializer(cabinet, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@extend_schema(
    parameters=[
        OpenApiParameter(name='cabinet_id', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),        
    ]
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cabinet_by_id(request, *args):
    """
    Get cabinet by id
    """
    queryset = []
    try:
        queryset = Cabinet.objects.all().filter(id=request.GET.get('cabinet_id'))
        if len(queryset) > 0:
            data = CabinetDetailsSerializer(queryset, many=True).data
            status_code = 200
    except Cabinet.DoesNotExist:
        pass
    except Exception as e:
        pass
    finally:
        return Response(data, status=status_code)
    
        
