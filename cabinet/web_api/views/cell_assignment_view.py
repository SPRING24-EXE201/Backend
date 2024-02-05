from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from cabinet.models import Cell
from order.models import OrderDetail, Assignment
from cabinet.web_api.serializers.cell_serializer import GetCellAssignmentRequestSerializer, GetCellAssignmentResponseSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

@extend_schema(
    parameters=[
        OpenApiParameter(name='cell_id', required=True, type=OpenApiTypes.INT32, location=OpenApiParameter.QUERY),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_cell_assignment(request):
    data = ''
    status_code = 400
    try:
        serializer = GetCellAssignmentRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            cell_id =  serializer.data.get('cell_id')

            access_token = request.auth
            user_id = access_token['user_id']

            time_now = timezone.now()
            order_detail =  OrderDetail.objects.get(cell__id=cell_id,
                                                     time_start__lte=time_now,
                                                     time_end__gte=time_now,
                                                     order__status=True,
                                                     user__id=user_id
                                                    )

            cell_assignment_serializer = GetCellAssignmentResponseSerializer(order_detail, many=False)
            data = cell_assignment_serializer.data
            status_code = 200

    except Cell.DoesNotExist:
        data = {'message': "Ô tủ không tồn tại"}
        status_code = 400
    except User.DoesNotExist:
        data = {'message': "Email không tồn tại"}
        status_code = 400
    except OrderDetail.DoesNotExist:
        data = {'message': "Người dùng không có quyền"}
        status_code = 400
    finally:
        return Response(data, status=status_code)
