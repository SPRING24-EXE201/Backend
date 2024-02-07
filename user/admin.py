from datetime import datetime

from django.contrib import admin

from user.models import User, Event


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'full_name', 'phone_number', 'address', 'image_link')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['eventType', 'timestamp', 'dataId', 'email', 'data']
    actions = ['admin_report']

    def admin_report(self, request, queryset):
        events = queryset.filter(eventType__in=['open', 'close'])
        report_data = []

        report_time = datetime.now()
        for time_type in ['month', 'day', 'hour']:
            if time_type == 'month':
                open_count = events.filter(eventType='open', timestamp__month=report_time.month).count()
                close_count = events.filter(eventType='close', timestamp__month=report_time.month).count()
                datetime_format = f"Tháng làm report: {report_time.month}"

            elif time_type == 'day':
                open_count = events.filter(eventType='open', timestamp__day=report_time.day).count()
                close_count = events.filter(eventType='close', timestamp__day=report_time.day).count()
                datetime_format = f"Ngày làm report: {report_time.day}"

            else:  # 'hour'
                open_count = events.filter(eventType='open', timestamp__hour=report_time.hour).count()
                close_count = events.filter(eventType='close', timestamp__hour=report_time.hour).count()
                datetime_format = f"Giờ làm report: {report_time.hour}"

            time_report = {
                'location': None,
                'time': datetime_format,
                'value': {
                    'open': open_count,
                    'close': close_count
                }
            }
            report_data.append(time_report)
        self.message_user(request, "Report generated.")

    admin_report.short_description = "Báo cáo về số lần đóng/mở tủ trong tháng/ngày/giờ làm báo cáo."