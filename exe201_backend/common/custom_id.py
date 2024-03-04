from django.db.models import Max
from django.template.defaultfilters import default


def location_custom_id():
    from location.models import Location
    id = Location.objects.all().count() + 1
    string_id = str(id)
    return string_id

def district_custom_id():
    from location.models import District
    id = District.objects.all().count() + 1
    string_id = str(id)
    return string_id

def province_custom_id():
    from location.models import Province
    id = Province.objects.all().count() + 1
    string_id = str(id)
    return string_id

def ward_custom_id():
    from location.models import Ward
    id = Ward.objects.all().count() + 1
    string_id = str(id)
    return string_id

def payment_order_id():
    from order.models import Order
    no = Order.objects.all().aggregate(Max('payment_order_id', default=70))
    if not no:
        return 70
    else:
        return no.get('payment_order_id__max') + 1
