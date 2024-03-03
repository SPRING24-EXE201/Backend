from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from cabinet.models import Cell
from user.models import User
from order.models import OrderDetail, Assignment
from cabinet.web_api.serializers.cell_serializer import (GetCellAssignmentRequestSerializer,
                                                         GetCellAssignmentResponseSerializer,
                                                         AssignCellToUserRequestSerializer)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.exceptions import PermissionDenied


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
            cell_id = serializer.data.get('cell_id')

            access_token = request.auth
            user_id = access_token['user_id']

            time_now = timezone.now()
            order_detail = OrderDetail.objects.get(cell__id=cell_id,
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


def validate_assignee(email, cell_id, assignee_email):
    if (email == assignee_email):
        raise PermissionDenied

    user_assignee = User.objects.get(email=assignee_email)

    cell_assigned = Cell.objects.get(id=cell_id)


def get_order_detail(email, user_id, cell_id, assignee_email):
    validate_assignee(email, cell_id, assignee_email)

    time_now = timezone.now()

    order_detail = OrderDetail.objects.get(cell__id=cell_id,
                                           time_start__lte=time_now,
                                           time_end__gte=time_now,
                                           order__status=True,
                                           user__id=user_id
                                           )
    return order_detail


def assign_cell(assignee):
    if not assignee:
        return None
    else:
        assignee.status = True
    assignee.save()
    return {'message': "Cấp quyền thành công"}


def unassign_cell(assignee):
    if not assignee:
        return None
    assignee.status = False
    assignee.save()
    return {'message': "Xóa quyền thành công"}


@extend_schema(
    request={'application/json': AssignCellToUserRequestSerializer}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_cell_to_user(request):
    try:
        data = {}
        status_code = 200
        serializer = AssignCellToUserRequestSerializer(data=request.data)
        if serializer.is_valid():
            cell_id = serializer.validated_data.get('cell_id')
            assignee_email = serializer.validated_data.get('assignee_email')
            status = serializer.validated_data.get('status')
            access_token = request.auth
            email = access_token['email']
            user_id = access_token['user_id']

            # validation
            order_detail = get_order_detail(email, user_id, cell_id, assignee_email)

            # use get here will automatically raise exception not exist
            assignee = Assignment.objects.filter(email=assignee_email, orderDetail__id=order_detail.id).first()
            if status:
                if not assignee:
                    assignee = Assignment()
                    assignee.email = assignee_email
                    assignee.orderDetail = order_detail
                if assignee.status:
                    data = {'message': 'Đã cấp quyền trước đó'}
                    status_code = 200
                else:
                    data = assign_cell(assignee)
            else:
                data = unassign_cell(assignee)
                if not data:
                   status_code = 404
                   data = {'message': 'Đã cấp quyền trước đó'}
    except PermissionDenied:
        data = {'message': "Không thể truy cập đến người thuê"}
        status_code = 400
    except User.DoesNotExist:
        data = {'message': "Người dùng không tồn tại"}
        status_code = 400
    except OrderDetail.DoesNotExist:
        data = {'message': "Tủ đã hết thời gian thuê"}
        status_code = 400
    except Cell.DoesNotExist:
        data = {'message': "Tủ không tồn tại"}
        status_code = 400
    return Response(data, status=status_code)
