import math

from django.db import transaction
from drf_spectacular.utils import extend_schema
from payos import ItemData, PaymentData
from payos.custom_error import PayOSError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cabinet.models import Cell, CostVersion, Campaign
from exe201_backend.common.constants import SystemConstants
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
    payos_response = None
    if serializer.is_valid(raise_exception=True):
        # Dummy payment_method = 1, waiting for implement payment
        new_order = Order(total_amount=0, payment_method=1, status=False)
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
        # Retry
        is_success = False
        for i in range(10):
            try:
                # Call PayOS to create purchase URL
                payos_items = [ItemData(name=detail.cell.__str__(), quantity=1, price=math.ceil(detail.sub_total))
                               for detail in order_detail_list]
                payment_data = PaymentData(orderCode=new_order.payment_order_id, amount=math.ceil(new_order.total_amount),
                                           description=f'Thuê {order_detail_list[0].cell.cabinet.description}',
                                           items=payos_items, cancelUrl=request.build_absolute_uri('/payos-purchase/cancel'),
                                           returnUrl=request.build_absolute_uri(f'/payos-purchase/success/{new_order.payment_order_id}'))
                payos_response = SystemConstants.payos_client.createPaymentLink(payment_data)
                is_success = True
                break
            except PayOSError as e:
                new_order.payment_order_id += 100
        if is_success:
            new_order.save()
            OrderDetail.objects.bulk_create(order_detail_list)
        else:
            raise
    return Response({
        'purchase_url': payos_response.checkoutUrl
    })
