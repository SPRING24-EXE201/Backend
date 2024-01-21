from urllib.parse import urlencode
from django.urls import reverse
from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        if 'page_size' in request.query_params:
            self.page_size = int(request.query_params['page_size'])
        if 'page' not in request.query_params:
            request.query_params['page'] = 1
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'totalPage': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'pageSize': self.page_size,
            'data': data
        })
