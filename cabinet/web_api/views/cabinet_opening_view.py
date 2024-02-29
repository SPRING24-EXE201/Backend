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
        user = request.user
        try:
            cell = Cell.objects.get(hash_code=hash_code)
            open_users = Utils.get_user_can_open_cell(hash_code)
            can_open = False
            if open_users:
                own_user = open_users.get('user_own_cell')
                assigned_users = open_users.get('assigned_users')
                if (own_user and own_user.id == user.id) or (assigned_users and user.email in assigned_users):
                    can_open = True
                    if user.email == own_user.email:
                        Utils.send_notification('Mở tủ thành công', f'{user.full_name} vừa mở {cell.__str__()}', None,
                                                user.id)
                    else:
                        Utils.send_notification('Mở tủ thành công', f'{user.full_name} vừa mở {cell.__str__()}', None,
                                                user.id)
                        Utils.send_notification('Mở tủ thành công', f'{user.full_name} vừa mở {cell.__str__()}', None,
                                                own_user.id)
                    Utils.send_command(hash_code)
                    data = 'Mở tủ thành công'
                    status_code = 200
            if not can_open:
                data = 'Không có quyền mở tủ'
                status_code = 403
        except Cell.DoesNotExist:
            data = 'Không tìm thấy ô tủ'
            status_code = 400
    return Response(status=status_code, data={
        'message': data
    })
