import os

from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view

from exe201_backend.common.constants import SystemConstants
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
    status = 200
    # Get Payment Info
    pay_os_info = SystemConstants.payos_client.getPaymentLinkInformation(payment_order_id)
    try:
        if pay_os_info and pay_os_info.status == 'PAID':
            user = Order.objects.get(payment_order_id=payment_order_id)

            status = 200
    except Order.DoesNotExist:
        status = 400
    return HttpResponse(status=status)
