from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from user.models import User
from user.web_api.serializers.user_serializer import UserSerializer, UpdateUserInformationRequestSerializer, UpdateUserInformationResponseSerializer


@api_view(['GET'])
def get_user(request):
    """
    Get all user
    """
    user = []
    try:
        user = User.objects.all().filter(is_active=True)
    except User.DoesNotExist:
        pass

    data = UserSerializer(user, many=True).data

    return Response({
        'success': True,
        'data': data,
    })

@extend_schema(
    request={'application/json': UpdateUserInformationRequestSerializer}
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    data = {}
    status_code = 200
    try:
        serializers = UpdateUserInformationRequestSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            access_token = request.auth
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            full_name = serializers.data.get('full_name')
            phone_number = serializers.data.get('phone_number')
            address = serializers.data.get('address')
            image_link = serializers.data.get('image_link')

            user.full_name = full_name
            user.phone_number = phone_number
            user.address = address
            user.image_link = image_link

            user.save()
            response_serializers = UpdateUserInformationResponseSerializer(instance=user)

            data = response_serializers.data
            status_code = 200
            
    except User.DoesNotExist as e:
        data = {'message': "User không tồn tại"}
        status_code = 400
    return JsonResponse(data, status=status_code)