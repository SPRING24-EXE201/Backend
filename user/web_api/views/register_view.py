from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from exe201_backend.common.utils import Utils
from user.models import User
from user.web_api.serializers.register_serializer import RegisterSerializer


@extend_schema(
    request={'application/json': RegisterSerializer}
)
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    status = 400
    data = {}
    if serializer.is_valid():
        email = serializer.data.get('email')
        try:
            user_exist = User.objects.get(email=serializer.data.get('email'))
            data = {
                'Message': 'Tài khoản đã tồn tại!'
            }
        except User.DoesNotExist:
            User.objects.create_user(email=email, password='')
            rs = Utils.send_otp(serializer.data.get('email'), 'đăng ký')
            if rs:
                data = {
                    'Message': 'Đăng ký thành công! Đã gửi mail OTP đăng nhập',
                }
                status = 200
    return Response(status=status, data=data)
