from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cabinet.models import Cell
from exe201_backend.common.utils import Utils
from order.web_api.serializers.valid_order_time_serializer import ValidOrderTimeRequestSerializer, ValidOrderSerializer, \
    ValidOrderTimeRequestListSerializer


@extend_schema(
    request={'application/json': ValidOrderTimeRequestListSerializer},
    methods=['POST'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_valid_order_time(request):
    serializer = ValidOrderTimeRequestListSerializer(data=request.data)
    response_data = {}
    status_code = 200
    if serializer.is_valid(raise_exception=True):
        valid_orders = ValidOrderSerializer(serializer.validated_data.get('valid_cells'), many=True)
        response_data = {
            'valid_orders': valid_orders.data,
            'invalid_orders': serializer.validated_data.get('invalid_cells')
        }
    return Response(response_data, status=status_code)
