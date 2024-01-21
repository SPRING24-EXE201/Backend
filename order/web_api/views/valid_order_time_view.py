from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cabinet.models import Cell
from exe201_backend.common.utils import Utils
from order.web_api.serializers.valid_order_time_serializer import ValidOrderTimeRequestSerializer, ValidOrderSerializer


@extend_schema(
    request={'application/json': ValidOrderTimeRequestSerializer(many=True)},
    methods=['POST'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_valid_order_time(request):
    serializer = ValidOrderTimeRequestSerializer(data=request.data, many=True)
    response_data = {}
    status_code = 200
    if serializer.is_valid(raise_exception=True):
        request_data = {}
        for item in list(serializer.data):
            if request_data.get(item.get('hash_code')):
                raise ValidationError({
                    'message': 'Trùng lặp thông tin ô tủ'
                })
            request_data[item.get('hash_code')] = {
                'time_start': item.get('time_start'),
                'time_end': item.get('time_end')
            }
        try:
            check_valid_data = Utils.check_valid_cells(request_data)
            valid_orders = ValidOrderSerializer(check_valid_data.get('valid_cells'), many=True)
            response_data = {
                'valid_orders': valid_orders.data,
                'invalid_orders': check_valid_data.get('invalid_cells')
            }
        except Cell.DoesNotExist:
            raise ValidationError({
                'message': 'Không tìm thấy ô tủ!'
            })
    return Response(response_data, status=status_code)
