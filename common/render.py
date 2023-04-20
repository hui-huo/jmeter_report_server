# _*_ coding: utf-8 _*_
"""
Time:     2023/3/31 10:03
Author:   Hui Huo.
File:     render.py
Describe: 
"""
from rest_framework.renderers import JSONRenderer


class CustomJSONRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        status_code = renderer_context['response'].status_code

        if 'code' in data:
            return super(CustomJSONRender, self).render(data, accepted_media_type, renderer_context)
        else:
            response = {
                'code': status_code,
                'msg': data,
                'data': None
            }
            return super(CustomJSONRender, self).render(response, accepted_media_type, renderer_context)
