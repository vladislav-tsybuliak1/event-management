from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EventPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = "per_page"
    max_page_size = 10

    def get_paginated_response(self, data: dict) -> Response:
        return Response(
            {
                "pages": self.page.paginator.num_pages,
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )