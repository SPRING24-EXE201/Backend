from payos import PayOS
from pytz import timezone

from exe201_backend import settings


class SystemConstants:
    otp_timeout = 300
    from_email_address = 'ibox.customerservice@gmail.com'
    timezone = timezone('Asia/Saigon')
    notification_config_type = 'Notification'
    controller_config_type = 'Controller'
    payos_client = PayOS(client_id=settings.PAYOS_CLIENT_ID, api_key=settings.PAYOS_API_KEY,
                         checksum_key=settings.PAYOS_CHECKSUM_KEY)