# _*_ coding: utf-8 _*_
"""
Time:     2023/4/4 13:33
Author:   Hui Huo.
File:     pagination.py
Describe: 
"""

# 分页使用，自定义一个分页类(三种)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from common.response import Response


class CommonPageNumberPagination(PageNumberPagination):
    page_num = 1
    page_size = 10  # 每页显示条数
    # page_query_param = 'page'  # page=10  查询第10页的数据，每页显示2条
    page_size_query_param = 'size'  # page=10&size=5    查询第10页，每页显示5条
    max_page_size = 50  # 每页最大显示条数
    allow_null = True

    @property
    def page(self):
        return self.page_num

    @page.setter
    def page(self, num):
        self.page_num = num

    def get_page_number(self, request, paginator):
        """
        重写获取page页数，默认从request中获取page参数
        :param request:
        :param paginator:
        :return:
        """
        return self.page_num

    def get_paginated_response(self, data):
        """
        重写响应格式
        :param data:
        :return:
        """
        return Response({
            # 'page_total': self.page.paginator.num_pages,
            'page': self.page.number,
            'size': self.page_size,
            'total': self.page.paginator.count,
            'results': data
        })


# LimitOffset
class CommonLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3  # 每页显示2条
    limit_query_param = 'limit'  # limit=3   取3条
    offset_query_param = 'offset'  # offset=1  从第一个位置开始，取limit条
    max_limit = 5
    # offset=3&limit=2      0  1 2 3 4 5
