import datetime
import random
from datetime import timedelta

from datetimerange import DateTimeRange
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from cabinet.models import CostVersion, Cell, CampaignCabinet
from exe201_backend.common.constants import SystemConstants
from order.models import OrderDetail


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
        cache.set(key=to_email, value=otp_code, timeout=SystemConstants.otp_timeout)

        msg = EmailMultiAlternatives(subject, html_body, SystemConstants.from_email_address, [to_email])
        msg.content_subtype = 'html'
        # Return number of message send success
        is_success = msg.send()
        if is_success == 0:
            return False
        return True

    @staticmethod
    def calc_total_cost_in_campaign(campaign, order_time_start, order_time_end):
        """
        Calculate total cost in a range of campaign
        :param campaign:
        :param order_time_start:
        :param order_time_end:
        :return: total_cost of an order
        :exception: CostVersion.DoesNotExist
        """
        last_hour = (order_time_end - order_time_start).total_seconds() / 3600.0
        total_cost = 0
        cost_versions = CostVersion.objects.filter(version=campaign.cost_version,
                                                   from_hour__lte=last_hour,
                                                   status=True).order_by('from_hour')
        if not cost_versions:
            raise CostVersion.DoesNotExist
        for version in cost_versions:
            from_hour = version.from_hour
            to_hour = version.to_hour
            # Normal version (from_hour, to_hour not null)
            if to_hour is not None:
                # Check last_hour is in range
                to_hour = last_hour if last_hour <= to_hour else to_hour
            # Last version case (to_hour = null)
            else:
                to_hour = last_hour
            duration_in_version = datetime.timedelta(hours=to_hour) - datetime.timedelta(hours=from_hour)
            total_cost += (duration_in_version.total_seconds() / version.unit.total_seconds()) * version.cost

        return round(total_cost, 0)

    @staticmethod
    def calc_total_cost_in_order_detail(hash_code, time_start, time_end):
        """
        :param: cell_id, time_start, time_end
        :return: total cost in order detail
        :exception: Cell.DoesNotExist, CampaignCabinet.DoesNotExist, CostVersion.DoesNotExist
        """
        total_cost = 0
        cell = Cell.objects.get(hash_code=hash_code)
        campaign_cabinets = (CampaignCabinet.objects.filter(cabinet__id=cell.cabinet.id,
                                                            campaign__status=True,
                                                            campaign__time_end__gte=time_start,
                                                            campaign__time_start__lte=time_end)
                             .select_related('campaign').order_by('campaign__time_start'))
        if not campaign_cabinets:
            raise CampaignCabinet.DoesNotExist
        campaigns = [campaign_cabinet.campaign for campaign_cabinet in campaign_cabinets]
        for valid_campaign in campaigns:
            total_cost += Utils.calc_total_cost_in_campaign(valid_campaign, time_start, time_end)
        return total_cost

    @staticmethod
    def check_valid_cells(data):
        """
        Get valid cell to rent in timerange
        :param data: list dict:
            [
                'hash_code_value':{
                                    'time_start': datetime,
                                    'time_end': datetime
                                  }
            ]
        :return: all valid cells, invalid cells in range
        :exception Cell.DoesNotExist
        """

        valid_cells = []
        invalid_cells = []
        try:
            order_detail_data = OrderDetail.objects.filter(cell__hash_code__in=data.keys(), order__status=True)
            if not order_detail_data:
                raise OrderDetail.DoesNotExist
            for key, value in data.items():
                needed_time_range = DateTimeRange(value['time_start'],
                                                  value['time_end'],
                                                  timezone=SystemConstants.timezone)
                order_details = [detail for detail in order_detail_data if detail.cell.hash_code == key]
                if not order_details:
                    raise OrderDetail.DoesNotExist
                overlap_details = []
                for time_detail in order_details:
                    detail_time_range = DateTimeRange(time_detail.time_start,
                                                      time_detail.time_end,
                                                      timezone=SystemConstants.timezone)
                    if needed_time_range.is_intersection(detail_time_range):
                        overlap_details.append(needed_time_range.intersection(detail_time_range))
                if len(overlap_details) == 0:
                    valid_cell = order_details[0].cell.__dict__
                    valid_cell['time_start'] = value['time_start']
                    valid_cell['time_end'] = value['time_end']
                    valid_cells.append(valid_cell)
                else:
                    invalid_cells.append(key)
        except OrderDetail.DoesNotExist:
            valid_cells = Cell.objects.filter(hash_code__in=list(data.keys()),
                                              status__gt=0)
            if not valid_cells:
                raise Cell.DoesNotExist
            valid_cells = [cell.__dict__.update({
                'time_start': data[cell.hash_code]['time_start'],
                'time_end': data[cell.hash_code]['time_end']
            }) for cell in valid_cells]
        return {
            'valid_cells': valid_cells,
            'invalid_cells': invalid_cells
        }

    @staticmethod
    def get_empty_cells_by_order_details(cell_id_list):
        """
        1. Check the cell is empty now
        :param cell_id_list: list of cell_id to check
        :return: empty cells number
        """
        if not cell_id_list:
            return 0
        now = timezone.now()
        # empty_cells = (OrderDetail.objects.filter(cell__id__in=cell_id_list,
        #                                           time_start__lte=now,
        #                                           time_end__gte=now,
        #                                           order__status=True)
        #                .values_list('cell', flat=True)).exclude()
        empty_cells = OrderDetail.objects.filter(cell__id__in=cell_id_list,
                                                 order__status=True).exclude(time_start__lt=now,
                                                                             time_end__gt=now)
        return len(empty_cells)

    @staticmethod
    def get_user_own_cell(cell_id):
        """
        Get user being in possession of cell
        :param cell_id: int
        :return: User
        """
        user = None
        if not cell_id:
            return None
        now = timezone.now()
        try:
            cell_order_now = OrderDetail.objects.get(cell__id=cell_id,
                                                     time_start__lte=now,
                                                     time_end__gte=now,
                                                     order__status=True)
            user = cell_order_now.user
        except OrderDetail.DoesNotExist:
            user = None
        return user

    @staticmethod
    def validate_order_time(time_start, time_end):
        """
        Validate new order time
        :param: time_start, time_end datetime
        :return: None if valid, errorMessage if invalid
        """
        if time_start < timezone.now():
            return 'Thời gian bắt đầu phải lớn hơn thời gian hiện tại'
        if time_start + timedelta(minutes=30) > time_end or (time_end - time_start).total_seconds() % 1800 != 0:
            return 'Khoảng thời gian không hợp lệ'
        return None
