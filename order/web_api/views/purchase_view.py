from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cabinet.models import Cell, CostVersion, Campaign
from exe201_backend.common.utils import Utils
from order.models import Order, OrderDetail
from order.web_api.serializers.purchase_serializer import PurchaseRequestListSerializer


@extend_schema(
    request={'application/json': PurchaseRequestListSerializer}
)
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def process_purchase(request):
    serializer = PurchaseRequestListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # Dummy payment_method = 1, waiting for implement payment
        new_order = Order(total_amount=0, payment_method=1, status=True)
        order_detail_list = []
        for detail in serializer.validated_data:
            hash_code = detail.get('hash_code')
            time_start = detail.get('start_date')
            time_end = detail.get('end_date')
            sub_total = 0
            error_message = None
            try:
                sub_total = Utils.calc_total_cost_in_order_detail(hash_code, time_start, time_end)
                # Plus to order total amount
                new_order.total_amount += sub_total
                # Add order detail
                order_detail = OrderDetail(order=new_order,
                                           cell=Cell.objects.get(hash_code=hash_code),
                                           user=request.user,
                                           time_start=time_start,
                                           time_end=time_end,
                                           sub_total=sub_total
                                           )
                order_detail_list.append(order_detail)
            except Cell.DoesNotExist:
                error_message = 'Không tìm thấy ô tủ!'
            except (Campaign.DoesNotExist, CostVersion.DoesNotExist):
                error_message = 'Không thể tính toán, vui lòng thử lại sau!'
            if error_message is not None:
                raise ValidationError({
                    'message': error_message
                })
        new_order.save()
        OrderDetail.objects.bulk_create(order_detail_list)
    return Response({
        'message': 'Thanh toán thành công!'
    })
