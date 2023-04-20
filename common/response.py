# _*_ coding: utf-8 _*_
"""
Time:     2023/4/4 14:02
Author:   Hui Huo.
File:     response.py
Describe: 
"""
from rest_framework.response import Response as HttpResponse


class Response(HttpResponse):
    def __init__(self, data=None, status=None, template_name=None, headers=None,
                 exception=False, content_type=None, msg=None):
        # 定义标准响应格式
        response_data = {
            'code': status or 200,
            'msg': msg or 'ok',
            'data': data
        }

        super().__init__(response_data, status=status, template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)
