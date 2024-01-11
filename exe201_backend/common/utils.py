import random

from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives

from exe201_backend.common.constants import SystemConstants


class Utils:
    @staticmethod
    def send_otp(to_email, action):
        otp_code = random.randint(100000, 999999)
        subject = 'Verification code from iBox'
        html_body = f"""<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
          <div style="margin:50px auto;width:70%;padding:20px 0">
            <div style="border-bottom:1px solid #eee">
              <a href="" style="font-size:1.4em;color: #1D9D6C;text-decoration:none;font-weight:600">iBox</a>
            </div>
            <p style="font-size:1.1em">Xin chào,</p>
            <p>Cảm ơn bạn đã tin dùng iBox. Hãy sử dụng OTP sau để hoàn thành quá trình {action} của bạn. OTP của bạn có hiệu lực trong {'%.0f' % (SystemConstants.otp_timeout / 60)} phút</p>
            <h2 style="background: #1D9D6C;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp_code}</h2>
            <p style="font-size:0.9em;">Trân trọng,<br />iBox</p>
            <hr style="border:none;border-top:1px solid #eee" />
            <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
              <p>iBox Inc</p>
              <p>Thủ Đức, Thành phố Hồ Chí Minh</p>
              <p>0987654321</p>
            </div>
          </div>
        </div>"""
        try:
            cache.set(key=to_email, value=otp_code, timeout=SystemConstants.otp_timeout)
            test = cache.get(to_email)
            msg = EmailMultiAlternatives(subject, html_body, SystemConstants.from_email_address, [to_email])
            msg.content_subtype = 'html'
            # Return number of message send success
            is_success = msg.send()
            if is_success == 0:
                return False
            return True
        except Exception as e:
            return False
