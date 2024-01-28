from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from exe201_backend import settings
from user.models import User
from user.web_api.serializers.otp_confirm_serializer import OtpConfirmSerializer


@extend_schema(
    request={'application/json': OtpConfirmSerializer}
)

@api_view(['POST'])
def otp_confirm(request):
    data = {}
    status_code = 200
    try:
        serializers = OtpConfirmSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            email = serializers.data.get('email')
            otp = serializers.data.get('otp')
            user = authenticate(email=email, otp=otp)
            if user is not None:
                login(request=request, backend=settings.AUTHENTICATION_BACKENDS[0], user=user)
                refresh = RefreshToken.for_user(user)
                refresh['name'] = user.full_name
                refresh['phone'] = user.phone_number
                refresh['email'] = user.email
                refresh['image_link'] = user.image_link
                data = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
                status_code = 200
            else:
                raise User.DoesNotExist
    except User.DoesNotExist as e:
        data = {'message': "Email không tồn tại"}
        status_code = 400
    return JsonResponse(data, status=status_code)

  