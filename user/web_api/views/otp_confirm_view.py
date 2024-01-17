from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from user.web_api.serializers.otp_confirm_serializer import OtpConfirmSerializer
from user.models import User

@api_view(['POST'])
def otp_confirm(request):
    try:
    
        serializers = OtpConfirmSerializer(data=request.data)
        if (serializers.is_valid()):
            email = serializers.data.get('email')
            otp = serializers.data.get('otp')

            if (cache.get(email) == otp):
                user = User.objects.get(email = email)
                refresh = RefreshToken.for_user(user)
                data = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
                status_code = 200
                user.refresh_token = str(refresh)
                user.save()
            else:
                raise Exception('OTP không khớp')
    except User.DoesNotExist as e:
        data = {'message': "Email không tồn tại"}
        status_code = 400
    except Exception as e:
        data = {'message': str(e)}
        status_code = 401
    finally: 
        return JsonResponse(data, status=status_code)