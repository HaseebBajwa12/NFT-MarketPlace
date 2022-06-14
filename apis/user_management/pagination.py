# from rest_framework import pagination
# from rest_framework.response import Response
#
#
# class MyPagination(pagination.PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 50
#     page_query_param = 'p'
#
#     def get_paginated_response(self, data):
#         response = Response(data)
#         response['count'] = self.page.paginator.count
#         response['next'] = self.get_next_link()
#         response['previous'] = self.get_previous_link()
#         return response


class PaginationHandlerMixin(object):
    def __init__(self):
        self._paginator = None

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
