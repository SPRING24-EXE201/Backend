from rest_framework.decorators import api_view
from rest_framework.response import Response

from order.models import OrderDetail
from order.web_api.serializers.order_detail_serializer import OrderDetailSerializer


from rest_framework.exceptions import NotFound

@api_view(['GET'])
def get_order_detail(request, order_id):
    """
    Get order detail by order_id
    """
    try:
        order_detail = OrderDetail.objects.filter(order_id=order_id, order_status=True)

        if not order_detail.exists():
            raise NotFound("Order Not Found")

        data = OrderDetailSerializer(order_detail, many=True).data

        return Response({
            'success': True,
            'data': data,
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
        })