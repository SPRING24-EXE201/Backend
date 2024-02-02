from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from exe201_backend.common.pagination import CustomPageNumberPagination
from order.models import Order
from order.web_api.serializers.order_serializer import OrderSerializer, OrderByUserSerializer, \
    OrderCellRequestSerializer


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    try:
        if request.method == 'GET':
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                except Order.DoesNotExist:
                    return Response({'error': 'Order not found'}, status=404)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=200)
        elif request.method == 'PUT':
            if order_id:
                serializer = OrderSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        # Check if the order exists
                        order = Order.objects.get(order_id=order_id)
                        # Update the order
                        serializer.update(order, serializer.validated_data)
                        return Response({'message': 'Order updated successfully!', 'order': serializer.data},
                                        status=200)
                    except Order.DoesNotExist:
                        return Response({'error': 'Order with id {} not found'.format(order_id)}, status=404)
                else:
                    return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    if order.status is None:
                        return Response({'error': 'Order status is None, cannot delete'}, status=400)
                    elif order.status:
                        order.status = False
                        order.save()
                        return Response({'message': 'Order deleted successfully!'}, status=200)
                    else:
                        return Response({'error': 'Order cannot be deleted because its status is already False'},
                                        status=400)
                except Order.DoesNotExist:
                    return Response({'error': 'Order not found'}, status=404)
            else:
                Order.objects.all().update(status=False)
                return Response({'message': 'All orders deleted successfully!'}, status=200)
    finally:
        pass


# @api_view('POST')
# @permission_classes([IsAuthenticated])
# def handle_orders(request):
#     # Get the token from the request headers
#     token = request.headers.get('Authorization')
#
#     # Remove 'Bearer ' from the token
#     token = token.split(' ')[1]
#
#     try:
#         # Decode the token to get the user_id
#         user_id = UntypedToken(token).payload['user_id']
#     except (InvalidToken, TokenError):
#         return Response({'error': 'Invalid token'}, status=400)
#
#     order_id = request.data.get('order_id')
#     total_amount = request.data.get('total_amount')
#     payment_method = request.data.get('payment_method')
#     order_date = request.data.get('order_date')
#     status = request.data.get('status')
#
#     # Check null values
#     if order_id is None or total_amount is None or payment_method is None or order_date is None or status is None:
#         return Response({'message': 'Invalid input. Please provide all required fields.'}, status=400)
#
#     # Check if order_id already exists
#     if Order.objects.filter(order_id=order_id).exists():
#         return Response({'message': 'Order with this order_id already exists.'}, status=400)
#
#     # Create new order
#     Order.objects.create(
#         id=order_id,
#         total_amount=total_amount,
#         payment_method=payment_method,
#         order_date=order_date,
#         status=status
#     )
#
#     return Response({'message': 'Order created successfully!'}, status=201)

@extend_schema(
    parameters=[OrderCellRequestSerializer],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    access_token = request.auth
    user_id = access_token['user_id']
    request_serializer = OrderCellRequestSerializer(data=request.query_params)
    response = {}
    paginator = CustomPageNumberPagination()
    if request_serializer.is_valid(raise_exception=True):
        orders = Order.objects.filter(orderdetail__user__id=user_id)
        time_start = request_serializer.data.get('start_date')
        time_end = request_serializer.data.get('end_date')
        cell_id = request_serializer.data.get('cell_id')
        is_desc = request_serializer.data.get('is_desc')
        if cell_id:
            orders = orders.filter(orderdetail__cell__id=cell_id)
        if time_start and time_end:
            orders = orders.filter(order_date__gte=time_start,
                                   order_date__lte=time_end)
        if is_desc:
            orders = orders.order_by('-order_date')
        else:
            orders = orders.order_by('order_date')
        if not orders:
            raise ValidationError({
                'message': 'Không tìm thấy thông tin'
            })
        serializer = OrderByUserSerializer(orders, many=True)

        response = paginator.paginate_queryset(serializer.data, request)

        # Return the serialized data
    return paginator.get_paginated_response(response)
