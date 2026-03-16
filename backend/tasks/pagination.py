from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    # 支持客户端通过page_size参数自定义每页条数
    page_size_query_param = 'page_size'
    # 最大每页条数
    max_page_size = 100
