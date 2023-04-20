# _*_ coding: utf-8 _*_
"""
Time:     2023/4/8 12:26
Author:   Hui Huo.
File:     filter.py
Describe: 
"""
import json

from django_filters.rest_framework import DjangoFilterBackend


class JSONFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_params = request.data
        if filter_params:
            try:
                filters_dict = json.loads(filter_params)
            except json.JSONDecodeError:
                filters_dict = {}
            queryset = queryset.filter(**filters_dict)
        return queryset
