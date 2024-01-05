from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from user.web_api.serializers.user_serializer import UserSerializer


@api_view(['GET'])
def get_user(request):
    """
    Get all user
    """
    user = []
    try:
        user = User.objects.all().filter(status=True)
    except User.DoesNotExist:
        pass

    data = UserSerializer(user, many=True).data

    return Response({
        'success': True,
        'data': data,
    })