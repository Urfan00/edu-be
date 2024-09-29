from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "page_count": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "page_size": self.page.paginator.per_page,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "has_next": self.page.has_next(),
            "has_previous": self.page.has_previous(),
            "start_index": self.page.start_index(),
            "end_index": self.page.end_index(),
            "results": data,
        })
