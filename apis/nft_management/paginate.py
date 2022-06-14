from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 6


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'

    def get_page_size(self, request):
        if self.page_size_query_param:
            print('qwerty')
            try:
                x = request.GET['limit']
                x = int(x)
                print(x)
                self.page_size = x
                return x
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data,result_key: str ="reslut"):
        return Response({
            'data': {
                # 'links': {
                #     'next': self.get_next_link(),
                #     'previous': self.get_previous_link()
                # },
                'pagination': {
                    'total': self.page.paginator.count,
                    'page': int(self.request.GET.get('page', DEFAULT_PAGE)),  # can not set default = self.page
                    # 'page_size': int(self.request.GET.get('page_size', self.page_size)),
                    'limit': self.page_size,
                },
                result_key: data,

            },
            'message': None,
            "status": True,

        }, status=status.HTTP_200_OK)