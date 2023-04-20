# _*_ coding: utf-8 _*_
"""
Time:     2023/4/20 17:15
Author:   Hui Huo.
File:     validator.py
Describe: 
"""
from rest_framework import serializers


class ChartDataSerializer(serializers.Serializer):
    project = serializers.CharField(required=False)
    env = serializers.CharField(required=False)
    type = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()


class LatestBuildSerializer(serializers.Serializer):
    project = serializers.CharField(required=False)
    env = serializers.CharField(required=False)


class SummaryFilterSerializer(serializers.Serializer):
    # page = serializers.IntegerField(default=1)
    # size = serializers.IntegerField(default=100)
    batch_no = serializers.CharField(required=False)
    project = serializers.CharField(required=False)
    env = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    pass_rate = serializers.CharField(required=False)
    result = serializers.CharField(required=False)
    start_time = serializers.CharField(required=False)
    end_time = serializers.CharField(required=False)


class SummaryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
