import os

from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view

from exe201_backend.common.constants import SystemConstants
from exe201_backend.common.utils import Utils
from order.models import Order


def get_json_file(request):
    # Đường dẫn tới tệp JSON
    json_file_path = os.path.join(os.path.dirname(__file__), 'assetlinks.json')

    # Kiểm tra xem tệp có tồn tại hay không
    if os.path.exists(json_file_path):
        # Mở tệp và trả về dưới dạng FileResponse
        return FileResponse(open(json_file_path, 'rb'), content_type='application/json')
    else:
        # Trả về một HttpResponse lỗi nếu tệp không tồn tại
        return HttpResponse("File not found", status=404)


@api_view(['GET'])
def success_payment(request, payment_order_id):
    status = 400
    # Get Payment Info
    pay_os_info = SystemConstants.payos_client.getPaymentLinkInformation(payment_order_id)
    try:
        if pay_os_info and pay_os_info.status == 'PAID':
            order = Order.objects.get(payment_order_id=payment_order_id)
            if not order.status:
                user = order.orderdetail_set.all()[0].user
                order.status = True
                order.save()
                # Send notification
                Utils.send_notification('Thanh toán thành công', f'Cảm ơn {user.full_name} đã tin dùng iBox', None,
                                        user.id)
                status = 200
    except Order.DoesNotExist:
        pass
    return HttpResponse(status=status)
