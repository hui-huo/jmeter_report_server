# _*_ coding: utf-8 _*_
"""
Time:     2023/4/4 13:33
Author:   Hui Huo.
File:     exception.py
Describe: 
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied

from rest_framework.views import exception_handler

from common.response import Response


def custom_exception_handler(exc, context):
    # 首先调用REST framework默认的异常处理，以获得标准的错误响应。
    # res = exception_handler(exc, context)

    if isinstance(exc, APIException):
        code = exc.status_code
        msg = exc.default_detail
        return Response(status=code, msg=msg)
    else:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        msg = exc.args
        return Response(status=code, msg=msg)


class ChartTypeError(APIException):
    status_code = 400
    default_detail = '类型错误[0 历史构建数据, 1 通过率数据]'
