from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cabinet.models import Cell
from cabinet.web_api.serializers.cabinet_opening_serializer import CabinetOpeningSerializerRequest
from exe201_backend.common.utils import Utils


@extend_schema(
    request=CabinetOpeningSerializerRequest
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_cabinet_opening_view(request):
    serializers = CabinetOpeningSerializerRequest(data=request.data)
    data = {}
    status_code = 200
    if serializers.is_valid(raise_exception=True):
        hash_code = serializers.data.get('hash_code')
        access_token = request.auth
        user_id = access_token['user_id']
        try:
            cell = Cell.objects.get(hash_code=hash_code)
            user_own_cell = Utils.get_user_own_cell(hash_code)
            if user_own_cell and user_own_cell.id == user_id:
                Utils.send_command(hash_code)
                data = 'Mở tủ thành công'
                status_code = 200
            else:
                data = 'Không có quyền mở tủ'
                status_code = 403
        except Cell.DoesNotExist:
            data = 'Không tìm thấy ô tủ'
            status_code = 400
    return Response(status=status_code, data={
        'message': data
    })
