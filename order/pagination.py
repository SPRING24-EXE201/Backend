from urllib.parse import urlencode
from django.urls import reverse
from rest_framework import pagination

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        self.max_page_size = queryset.count() // self.page_size
        return super().paginate_queryset(queryset, request, view)
    
    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri(reverse('order_by_user'))
        page_size = self.get_page_size(self.request)
        page_number = self.page.next_page_number()
        return f'{url}?{urlencode({"page_size": page_size, "page": page_number})}'