from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone

from location.models import Location
from order.models import Event
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth


# Create your views here.
def purchase(request):
    chart_base_field = request.GET.get('chart-base-field', 'time')
    time_type = request.GET.get('time-type', None)
    start_date = request.GET.get('start-date', None)
    end_date = request.GET.get('end-date', None)
    start_time = request.GET.get('start-time', None)
    end_time = request.GET.get('end-time', None)
    location_ids = request.GET.get('selected-location', None)

    events_purchase_success = []
    events_purchase_failure = []
    label_chart = ""
    time_type_string = ""
    chart_name = ["Giao dịch thành công", "Giao dịch thất bại"]
    chart_title = "BIỂU ĐỒ GIAO DỊCH"
    location_list_render = []
    selected_location = []
    start_datetime_str = ""
    end_datetime_str = ""
    start_time_str = ""
    end_time_str = ""

    if chart_base_field == "time":
        if time_type is None:
            time_type = "date"

        if time_type == "hours":
            if start_date is None:
                start_date = f'01-{datetime.now().month}-{datetime.now().year}'

            if end_date is None:
                end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

            if start_time is None:
                start_time = "00:00"

            if end_time is None:
                end_time = "23:59"

            # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
            try:
                start_datetime = datetime.strptime(f'{start_date} {start_time}', "%d-%m-%Y %H:%M")
                end_datetime = datetime.strptime(f'{end_date} {end_time}', "%d-%m-%Y %H:%M")
                start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
                labels = get_hour_list(f'{start_datetime.strftime("%d-%m-%Y %H:%M")}',
                                       f'{end_datetime.strftime("%d-%m-%Y %H:%M")}')
            except ValueError:
                print("Thời gian không hợp lệ")
                return render(request, 'chartapp/index.html', {'error_message': "Thời gian không hợp lệ"})

            start_time_str = f'{start_datetime.strftime("%H:%M")}'
            end_time_str = f'{end_datetime.strftime("%H:%M")}'

            start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thành công
            events_data_purchase_success = Event.objects.filter(orderDetail__order__status=True,
                                                                eventType='purchase',
                                                                timestamp__range=(start_datetime, end_datetime)) \
                .annotate(hour=TruncDay('timestamp')) \
                .values('hour') \
                .annotate(event_count=Count('id'))

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thất bại
            events_data_purchase_failure = Event.objects.filter(orderDetail__order__status=False,
                                                                eventType='purchase',
                                                                timestamp__range=(start_datetime, end_datetime)) \
                .annotate(hour=TruncDay('timestamp')) \
                .values('hour') \
                .annotate(event_count=Count('id'))

            # Định dạng dữ liệu để trả về dưới dạng danh sách các object với trường x là ngày và trường y là số lượng sự kiện
            events_dict_purchase_success = {event['hour'].strftime('%d-%m-%Y %H:%M'): event['event_count'] for event in
                                            events_data_purchase_success}
            events_dict_purchase_failure = {event['hour'].strftime('%d-%m-%Y %H:%M'): event['event_count'] for event in
                                            events_data_purchase_failure}

            # Duyệt qua mỗi ngày trong labels và kiểm tra xem có sự kiện tương ứng không, nếu không thì thêm một sự kiện mới với y là 0
            for label in labels:
                if label not in events_dict_purchase_success:
                    events_purchase_success.append({'x': label, 'y': 0})
                else:
                    events_purchase_success.append({'x': label, 'y': events_dict_purchase_success[label]})

                if label not in events_dict_purchase_failure:
                    events_purchase_failure.append({'x': label, 'y': 0})
                else:
                    events_purchase_failure.append({'x': label, 'y': events_dict_purchase_failure[label]})

            time_type_string = "Giờ"

        # Nếu người dùng chọn biểu đồ theo thời gian
        elif time_type == "date":

            if start_date is None:
                start_date = f'01-{datetime.now().month}-{datetime.now().year}'

            if end_date is None:
                end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

            # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
            try:
                start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
                end_datetime = datetime.strptime(end_date, "%d-%m-%Y")
                start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
            except ValueError:
                return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

            start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'

            labels = [(start_datetime + timezone.timedelta(days=i)).strftime("%d-%m-%Y") for i in
                      range((end_datetime - start_datetime).days + 1)]

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thành công
            events_data_purchase_success = Event.objects.filter(orderDetail__order__status=True,
                                                                eventType='purchase',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(date=TruncDay('timestamp')) \
                .values('date') \
                .annotate(event_count=Count('id'))

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thất bại
            events_data_purchase_failure = Event.objects.filter(orderDetail__order__status=False,
                                                                eventType='purchase',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(date=TruncDay('timestamp')) \
                .values('date') \
                .annotate(event_count=Count('id'))

            # Định dạng dữ liệu để trả về dưới dạng danh sách các object với trường x là ngày và trường y là số lượng sự kiện
            events_dict_purchase_success = {event['date'].strftime('%d-%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_success}
            events_dict_purchase_failure = {event['date'].strftime('%d-%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_failure}

            # Duyệt qua mỗi ngày trong labels và kiểm tra xem có sự kiện tương ứng không, nếu không thì thêm một sự kiện mới với y là 0
            for label in labels:
                if label not in events_dict_purchase_success:
                    events_purchase_success.append({'x': label, 'y': 0})
                else:
                    events_purchase_success.append({'x': label, 'y': events_dict_purchase_success[label]})

                if label not in events_dict_purchase_failure:
                    events_purchase_failure.append({'x': label, 'y': 0})
                else:
                    events_purchase_failure.append({'x': label, 'y': events_dict_purchase_failure[label]})

            time_type_string = "Ngày"

        elif time_type == "month":

            if start_date is None:
                start_date = f'01-{datetime.now().year}'

            if end_date is None:
                end_date = f'12-{datetime.now().year}'

            try:
                # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
                start_datetime = datetime.strptime(start_date, "%m-%Y")
                end_datetime = datetime.strptime(end_date, "%m-%Y")
                labels = get_month_list(f"{start_datetime.month}-{start_datetime.year}",
                                        f"{end_datetime.month}-{end_datetime.year}")
                start_datetime = timezone.make_aware(start_datetime)
                end_datetime = timezone.make_aware(end_datetime)
            except ValueError:
                return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

            start_datetime_str = f'{start_datetime.strftime("%Y-%m")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m")}'

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và thành công
            events_data_purchase_success = Event.objects.filter(orderDetail__order__status=True,
                                                                eventType='purchase',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(month=TruncMonth('timestamp')) \
                .values('month') \
                .annotate(event_count=Count('id'))

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và thất bại
            events_data_purchase_failure = Event.objects.filter(orderDetail__order__status=False,
                                                                eventType='purchase',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(month=TruncMonth('timestamp')) \
                .values('month') \
                .annotate(event_count=Count('id'))

            # Định dạng dữ liệu để trả về dưới dạng danh sách các object với trường x là tháng và trường y là số lượng sự kiện
            events_dict_purchase_success = {event['month'].strftime('%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_success}
            events_dict_purchase_failure = {event['month'].strftime('%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_failure}

            # Duyệt qua mỗi ngày trong labels và kiểm tra xem có sự kiện tương ứng không, nếu không thì thêm một sự kiện mới với y là 0
            for label in labels:
                if label not in events_dict_purchase_success:
                    events_purchase_success.append({'x': label, 'y': 0})
                else:
                    events_purchase_success.append({'x': label, 'y': events_dict_purchase_success[label]})

                if label not in events_dict_purchase_failure:
                    events_purchase_failure.append({'x': label, 'y': 0})
                else:
                    events_purchase_failure.append({'x': label, 'y': events_dict_purchase_failure[label]})

            time_type_string = "Tháng"

        label_chart = "Giao dịch thành công theo thời gian"

    if chart_base_field == "location":
        events_data_purchase_success = []
        events_data_purchase_failure = []

        if time_type is None:
            time_type = "all"

        if location_ids is None:
            location_list = Location.objects.all()
            location_ids = [location.id for location in location_list]
            selected_location = location_ids
        else:
            location_ids = location_ids.split(',')
            selected_location = location_ids
        label_chart = "Giao dịch thành công theo địa điểm"

        for location in Location.objects.all():
            location_item = Location.objects.get(id=location.id)
            location_list_render.append({'id': location.id, 'name': location_item.get_display_name()})

        for location_id in location_ids:

            if time_type == "hours":
                if start_date is None:
                    start_date = f'01-{datetime.now().month}-{datetime.now().year}'

                if end_date is None:
                    end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

                if start_time is None:
                    start_time = "00:00"

                if end_time is None:
                    end_time = "23:59"

                # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
                try:
                    start_datetime = datetime.strptime(f'{start_date} {start_time}', "%d-%m-%Y %H:%M")
                    end_datetime = datetime.strptime(f'{end_date} {end_time}', "%d-%m-%Y %H:%M")
                    start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                    end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
                    labels = get_hour_list(f'{start_datetime.strftime("%d-%m-%Y %H:%M")}',
                                           f'{end_datetime.strftime("%d-%m-%Y %H:%M")}')
                except ValueError:
                    print("Thời gian không hợp lệ")
                    return render(request, 'chartapp/index.html', {'error_message': "Thời gian không hợp lệ"})

                start_time_str = f'{start_datetime.strftime("%H:%M")}'
                end_time_str = f'{end_datetime.strftime("%H:%M")}'

                start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
                end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'

                events_data_purchase_success = Event.objects.filter(
                    orderDetail__order__status=True,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase',
                    timestamp__range=(start_datetime, end_datetime))

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__order__status=False,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase',
                    timestamp__range=(start_datetime, end_datetime))

            elif time_type == "date":

                if start_date is None:
                    start_date = f'01-{datetime.now().month}-{datetime.now().year}'

                if end_date is None:
                    end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

                try:
                    if start_date is not None and end_date is not None:
                        start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
                        end_datetime = datetime.strptime(end_date, "%d-%m-%Y")
                        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
                except ValueError:
                    return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

                events_data_purchase_success = Event.objects.filter(
                    orderDetail__order__status=True,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase',
                    timestamp__date__range=(start_datetime, end_datetime))

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__order__status=False,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase',
                    timestamp__date__range=(start_datetime, end_datetime))

            elif time_type == "month":
                if start_date is None:
                    start_date = f'01-{datetime.now().year}'

                if end_date is None:
                    end_date = f'12-{datetime.now().year}'

                try:
                    if start_date is not None and end_date is not None:
                        start_datetime = datetime.strptime(start_date, "%m-%Y")
                        end_datetime = datetime.strptime(end_date, "%m-%Y")
                        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())

                except ValueError:
                    return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

                events_data_purchase_success = Event.objects.filter(
                    orderDetail__order__status=True,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase',
                    timestamp__date__range=(start_datetime, end_datetime))

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__order__status=False,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase',
                    timestamp__date__range=(start_datetime, end_datetime))

            elif time_type == "all":
                events_data_purchase_success = Event.objects.filter(
                    orderDetail__order__status=True,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase')

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__order__status=False,
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='purchase')

            location = Location.objects.get(id=location_id)
            events_purchase_success.append(
                {'x': location.get_display_name(), 'y': events_data_purchase_success.count()})
            events_purchase_failure.append(
                {'x': location.get_display_name(), 'y': events_data_purchase_failure.count()})

        if start_date is not None and time_type == 'date':
            start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'
        elif end_date is not None and time_type == 'month':
            start_datetime_str = f'{start_datetime.strftime("%Y-%m")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m")}'

    context = {
        "chart_base_field": chart_base_field,
        "events": [events_purchase_success, events_purchase_failure],
        "label": label_chart,
        "time_type_string": time_type_string,
        "chart_title": chart_title,
        "chart_name": chart_name,
        "chart_base_field": chart_base_field,
        "time_type": time_type,
        "location_list_render": location_list_render,
        "selected_location": selected_location,
        "start_datetime": start_datetime_str,
        "end_datetime": end_datetime_str,
        "start_time": start_time_str,
        "end_time": end_time_str,
    }

    return render(request, 'chartapp/index.html', context)


def box_event(request):
    chart_type = request.GET.get('chart-type', 'bar')
    chart_base_field = request.GET.get('chart-base-field', 'time')
    time_type = request.GET.get('time-type', None)
    start_date = request.GET.get('start-date', None)
    end_date = request.GET.get('end-date', None)
    start_time = request.GET.get('start-time', None)
    end_time = request.GET.get('end-time', None)
    location_ids = request.GET.get('selected-location', None)

    events_purchase_success = []
    events_purchase_failure = []
    label_chart = ""
    time_type_string = ""
    chart_name = ["Giao dịch thành công", "Giao dịch thất bại"]
    chart_title = "BIỂU ĐỒ TƯƠNG TÁC TỦ"
    location_list_render = []
    selected_location = []
    start_datetime_str = ""
    end_datetime_str = ""
    start_time_str = ""
    end_time_str = ""

    if chart_base_field == "time":
        if time_type is None:
            time_type = "date"

        if time_type == "hours":
            if start_date is None:
                start_date = f'01-{datetime.now().month}-{datetime.now().year}'

            if end_date is None:
                end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

            if start_time is None:
                start_time = "00:00"

            if end_time is None:
                end_time = "23:59"

            # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
            try:
                start_datetime = datetime.strptime(f'{start_date} {start_time}', "%d-%m-%Y %H:%M")
                end_datetime = datetime.strptime(f'{end_date} {end_time}', "%d-%m-%Y %H:%M")
                start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
                labels = get_hour_list(f'{start_datetime.strftime("%d-%m-%Y %H:%M")}',
                                       f'{end_datetime.strftime("%d-%m-%Y %H:%M")}')
            except ValueError:
                print("Thời gian không hợp lệ")
                return render(request, 'chartapp/index.html', {'error_message': "Thời gian không hợp lệ"})

            start_time_str = f'{start_datetime.strftime("%H:%M")}'
            end_time_str = f'{end_datetime.strftime("%H:%M")}'

            start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thành công
            events_data_purchase_success = Event.objects.filter(
                                                                eventType='open',
                                                                timestamp__range=(start_datetime, end_datetime)) \
                .annotate(hour=TruncDay('timestamp')) \
                .values('hour') \
                .annotate(event_count=Count('id'))

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thất bại
            events_data_purchase_failure = Event.objects.filter(
                                                                eventType='close',
                                                                timestamp__range=(start_datetime, end_datetime)) \
                .annotate(hour=TruncDay('timestamp')) \
                .values('hour') \
                .annotate(event_count=Count('id'))

            # Định dạng dữ liệu để trả về dưới dạng danh sách các object với trường x là ngày và trường y là số lượng sự kiện
            events_dict_purchase_success = {event['hour'].strftime('%d-%m-%Y %H:%M'): event['event_count'] for event in
                                            events_data_purchase_success}
            events_dict_purchase_failure = {event['hour'].strftime('%d-%m-%Y %H:%M'): event['event_count'] for event in
                                            events_data_purchase_failure}

            # Duyệt qua mỗi ngày trong labels và kiểm tra xem có sự kiện tương ứng không, nếu không thì thêm một sự kiện mới với y là 0
            for label in labels:
                if label not in events_dict_purchase_success:
                    events_purchase_success.append({'x': label, 'y': 0})
                else:
                    events_purchase_success.append({'x': label, 'y': events_dict_purchase_success[label]})

                if label not in events_dict_purchase_failure:
                    events_purchase_failure.append({'x': label, 'y': 0})
                else:
                    events_purchase_failure.append({'x': label, 'y': events_dict_purchase_failure[label]})

            time_type_string = "Giờ"

        # Nếu người dùng chọn biểu đồ theo thời gian
        elif time_type == "date":

            if start_date is None:
                start_date = f'01-{datetime.now().month}-{datetime.now().year}'

            if end_date is None:
                end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

            # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
            try:
                start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
                end_datetime = datetime.strptime(end_date, "%d-%m-%Y")
                start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
            except ValueError:
                return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

            start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'

            labels = [(start_datetime + timezone.timedelta(days=i)).strftime("%d-%m-%Y") for i in
                      range((end_datetime - start_datetime).days + 1)]

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thành công
            events_data_purchase_success = Event.objects.filter(
                                                                eventType='open',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(date=TruncDay('timestamp')) \
                .values('date') \
                .annotate(event_count=Count('id'))

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và giao dịch thất bại
            events_data_purchase_failure = Event.objects.filter(
                                                                eventType='close',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(date=TruncDay('timestamp')) \
                .values('date') \
                .annotate(event_count=Count('id'))

            # Định dạng dữ liệu để trả về dưới dạng danh sách các object với trường x là ngày và trường y là số lượng sự kiện
            events_dict_purchase_success = {event['date'].strftime('%d-%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_success}
            events_dict_purchase_failure = {event['date'].strftime('%d-%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_failure}

            # Duyệt qua mỗi ngày trong labels và kiểm tra xem có sự kiện tương ứng không, nếu không thì thêm một sự kiện mới với y là 0
            for label in labels:
                if label not in events_dict_purchase_success:
                    events_purchase_success.append({'x': label, 'y': 0})
                else:
                    events_purchase_success.append({'x': label, 'y': events_dict_purchase_success[label]})

                if label not in events_dict_purchase_failure:
                    events_purchase_failure.append({'x': label, 'y': 0})
                else:
                    events_purchase_failure.append({'x': label, 'y': events_dict_purchase_failure[label]})

            time_type_string = "Ngày"

        elif time_type == "month":

            if start_date is None:
                start_date = f'01-{datetime.now().year}'

            if end_date is None:
                end_date = f'12-{datetime.now().year}'

            try:
                # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
                start_datetime = datetime.strptime(start_date, "%m-%Y")
                end_datetime = datetime.strptime(end_date, "%m-%Y")
                labels = get_month_list(f"{start_datetime.month}-{start_datetime.year}",
                                        f"{end_datetime.month}-{end_datetime.year}")
                start_datetime = timezone.make_aware(start_datetime)
                end_datetime = timezone.make_aware(end_datetime)
            except ValueError:
                return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

            start_datetime_str = f'{start_datetime.strftime("%Y-%m")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m")}'

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và thành công
            events_data_purchase_success = Event.objects.filter(eventType='open',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(month=TruncMonth('timestamp')) \
                .values('month') \
                .annotate(event_count=Count('id'))

            # Truy vấn các sự kiện trong khoảng thời gian đã cho và nhóm chúng theo ngày và thất bại
            events_data_purchase_failure = Event.objects.filter(eventType='close',
                                                                timestamp__date__range=(start_datetime, end_datetime)) \
                .annotate(month=TruncMonth('timestamp')) \
                .values('month') \
                .annotate(event_count=Count('id'))

            # Định dạng dữ liệu để trả về dưới dạng danh sách các object với trường x là tháng và trường y là số lượng sự kiện
            events_dict_purchase_success = {event['month'].strftime('%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_success}
            events_dict_purchase_failure = {event['month'].strftime('%m-%Y'): event['event_count'] for event in
                                            events_data_purchase_failure}

            # Duyệt qua mỗi ngày trong labels và kiểm tra xem có sự kiện tương ứng không, nếu không thì thêm một sự kiện mới với y là 0
            for label in labels:
                if label not in events_dict_purchase_success:
                    events_purchase_success.append({'x': label, 'y': 0})
                else:
                    events_purchase_success.append({'x': label, 'y': events_dict_purchase_success[label]})

                if label not in events_dict_purchase_failure:
                    events_purchase_failure.append({'x': label, 'y': 0})
                else:
                    events_purchase_failure.append({'x': label, 'y': events_dict_purchase_failure[label]})

            time_type_string = "Tháng"

        label_chart = "Giao dịch thành công theo thời gian"

    if chart_base_field == "location":
        events_data_purchase_success = []
        events_data_purchase_failure = []

        if time_type is None:
            time_type = "all"

        if location_ids is None:
            location_list = Location.objects.all()
            location_ids = [location.id for location in location_list]
            selected_location = location_ids
        else:
            location_ids = location_ids.split(',')
            selected_location = location_ids
        label_chart = "Giao dịch thành công theo địa điểm"

        for location in Location.objects.all():
            location_item = Location.objects.get(id=location.id)
            location_list_render.append({'id': location.id, 'name': location_item.get_display_name()})

        for location_id in location_ids:

            if time_type == "hours":
                if start_date is None:
                    start_date = f'01-{datetime.now().month}-{datetime.now().year}'

                if end_date is None:
                    end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

                if start_time is None:
                    start_time = "00:00"

                if end_time is None:
                    end_time = "23:59"

                # Chuyển đổi ngày bắt đầu và kết thúc từ string sang datetime
                try:
                    start_datetime = datetime.strptime(f'{start_date} {start_time}', "%d-%m-%Y %H:%M")
                    end_datetime = datetime.strptime(f'{end_date} {end_time}', "%d-%m-%Y %H:%M")
                    start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                    end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
                    labels = get_hour_list(f'{start_datetime.strftime("%d-%m-%Y %H:%M")}',
                                           f'{end_datetime.strftime("%d-%m-%Y %H:%M")}')
                except ValueError:
                    print("Thời gian không hợp lệ")
                    return render(request, 'chartapp/index.html', {'error_message': "Thời gian không hợp lệ"})

                start_time_str = f'{start_datetime.strftime("%H:%M")}'
                end_time_str = f'{end_datetime.strftime("%H:%M")}'

                start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
                end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'

                events_data_purchase_success = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='open',
                    timestamp__range=(start_datetime, end_datetime))

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='close',
                    timestamp__range=(start_datetime, end_datetime))

            elif time_type == "date":

                if start_date is None:
                    start_date = f'01-{datetime.now().month}-{datetime.now().year}'

                if end_date is None:
                    end_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year}'

                try:
                    if start_date is not None and end_date is not None:
                        start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
                        end_datetime = datetime.strptime(end_date, "%d-%m-%Y")
                        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
                except ValueError:
                    return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

                events_data_purchase_success = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='open',
                    timestamp__date__range=(start_datetime, end_datetime))

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='close',
                    timestamp__date__range=(start_datetime, end_datetime))

            elif time_type == "month":
                if start_date is None:
                    start_date = f'01-{datetime.now().year}'

                if end_date is None:
                    end_date = f'12-{datetime.now().year}'

                try:
                    if start_date is not None and end_date is not None:
                        start_datetime = datetime.strptime(start_date, "%m-%Y")
                        end_datetime = datetime.strptime(end_date, "%m-%Y")
                        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
                        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())

                except ValueError:
                    return render(request, 'chartapp/index.html', {'error': 'Invalid date format'})

                events_data_purchase_success = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='open',
                    timestamp__date__range=(start_datetime, end_datetime))

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='close',
                    timestamp__date__range=(start_datetime, end_datetime))

            elif time_type == "all":
                events_data_purchase_success = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='open')

                events_data_purchase_failure = Event.objects.filter(
                    orderDetail__cell__cabinet__controller__location__id=location_id,
                    eventType='close')

            location = Location.objects.get(id=location_id)
            events_purchase_success.append(
                {'x': location.get_display_name(), 'y': events_data_purchase_success.count()})
            events_purchase_failure.append(
                {'x': location.get_display_name(), 'y': events_data_purchase_failure.count()})

        if start_date is not None and time_type == 'date':
            start_datetime_str = f'{start_datetime.strftime("%Y-%m-%d")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m-%d")}'
        elif end_date is not None and time_type == 'month':
            start_datetime_str = f'{start_datetime.strftime("%Y-%m")}'
            end_datetime_str = f'{end_datetime.strftime("%Y-%m")}'

    context = {
        "chart_base_field": chart_base_field,
        "events": [events_purchase_success, events_purchase_failure],
        "label": label_chart,
        "time_type_string": time_type_string,
        "chart_type": chart_type,
        "chart_title": chart_title,
        "chart_name": chart_name,
        "chart_base_field": chart_base_field,
        "time_type": time_type,
        "location_list_render": location_list_render,
        "selected_location": selected_location,
        "start_datetime": start_datetime_str,
        "end_datetime": end_datetime_str,
        "start_time": start_time_str,
        "end_time": end_time_str,
    }

    return render(request, 'chartapp/index.html', context)


def get_month_list(start_month, end_month):
    # Chuyển đổi start_month và end_month thành datetime objects
    start_datetime = datetime.strptime(start_month, "%m-%Y")
    end_datetime = datetime.strptime(end_month, "%m-%Y")

    # Tạo danh sách các tháng
    month_list = []
    current_datetime = start_datetime

    while current_datetime <= end_datetime:
        month_list.append(current_datetime.strftime("%m-%Y"))
        # Tăng thời gian lên 1 tháng
        if current_datetime.month == 2 and current_datetime.year % 4 == 0 and (
                current_datetime.year % 100 != 0 or current_datetime.year % 400 == 0):  # Trường hợp năm nhuận
            next_month = current_datetime.replace(day=29) + timedelta(
                days=4)  # Đặt ngày là 29, sau đó thêm 4 ngày để có được tháng tiếp theo
            current_datetime = next_month.replace(day=1)
        elif current_datetime.month == 2:  # Trường hợp tháng 2 không phải năm nhuận
            next_month = current_datetime.replace(day=28) + timedelta(
                days=4)  # Đặt ngày là 28, sau đó thêm 4 ngày để có được tháng tiếp theo
            current_datetime = next_month.replace(day=1)
        else:
            current_datetime = (current_datetime + timedelta(days=32)).replace(day=1)

    return month_list


from datetime import datetime, timedelta


def get_hour_list(start_time, end_time):
    start_datetime = datetime.strptime(start_time, "%d-%m-%Y %H:%M")
    end_datetime = datetime.strptime(end_time, "%d-%m-%Y %H:%M")

    hour_list = []
    current_datetime = start_datetime

    while current_datetime <= end_datetime:
        hour_list.append(current_datetime.strftime("%d-%m-%Y %H:%M"))
        current_datetime += timedelta(hours=1)

    return hour_list
