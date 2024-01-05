from rest_framework.decorators import api_view
from rest_framework.response import Response

from order.models import OrderDetail
from order.web_api.serializers.order_detail_serializer import OrderDetailSerializer


@api_view(['GET'])
def get_order_detail(request):
    """
    Get all order detail
    """
    order_detail = []
    try:
        order_detail = OrderDetail.objects.all().filter(status=True)
    except OrderDetail.DoesNotExist:
        pass

    data = OrderDetailSerializer(order_detail, many=True).data

    return Response({
        'success': True,
        'data': data,
    })