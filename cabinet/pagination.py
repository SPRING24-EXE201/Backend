from urllib.parse import urlencode
from django.urls import reverse
from rest_framework import pagination

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        return super().paginate_queryset(queryset, request, view)

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri(reverse('get_cabinet'))
        page_size = self.get_page_size(self.request)
        page_number = self.page.next_page_number()
        pos_x = self.request.query_params.get('pos_x', None)
        pos_y = self.request.query_params.get('pos_y', None)
        return f'{url}?{urlencode({"pos_x": pos_x, "pos_y": pos_y, "page_size": page_size, "page": page_number})}'
