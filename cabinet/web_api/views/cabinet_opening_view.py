from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from cabinet.models import Cell
from django.core.exceptions import PermissionDenied
from cabinet.web_api.serializers.cabinet_opening_serializer import CabinetOpeningSerializerRequest, CabinetOpeningSerializerResponse
from exe201_backend import service_bus
@extend_schema(
    request = CabinetOpeningSerializerRequest
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_cabinet_opening_view(request):
    try:
        serializers = CabinetOpeningSerializerRequest(data=request.data)
        if serializers.is_valid():
            hash_code = serializers.data.get('hash_code')
            access_token = request.auth
            user_id = access_token['user_id']
            cell = Cell.objects.get(hash_code=hash_code)

            if user_id == cell.user:
                controller = cell.cabinet.controller
                json_data = {"controller_id": controller.id, "cabinet_id": cell.cabinet_id, "cell_index": cell.cell_index}
                data = CabinetOpeningSerializerResponse(json_data, many = False ).data
                service_bus.handler_message(str(json_data))
                status_code = 200
            else:
                raise PermissionDenied("Không có quyên truy cập")
    except Cell.DoesNotExist:
        data = {'message': "Ô tủ không tồn tại"}
        status_code = 400
    except PermissionDenied as e:
        data = {'message': str(e)}
        status_code = 403
    except Exception as e:
        data = {'message': "Lỗi hệ thống"}
        status_code = 500
    finally:
        return JsonResponse(data, status=status_code)