# _*_ coding: utf-8 _*_
"""
Time:     2023/4/10 11:33
Author:   Hui Huo.
File:     serializer.py
Describe: 序列化
"""

import datetime
import re

from django.forms import model_to_dict
from rest_framework import serializers

from app.models import TestSummary, TestCase
from common.utils import generate_unique_id


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TestSummarySerializer(DynamicFieldsModelSerializer):
    def to_representation(self, instance):
        if not instance:
            return instance
        data = super().to_representation(instance)
        if data.get('start_time'):
            start_dt = datetime.datetime.fromtimestamp(int(data.get('start_time')) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.datetime.fromtimestamp(int(data.get('end_time')) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            data['start_time'] = start_dt
            data['end_time'] = end_dt
        return data

    class Meta:
        model = TestSummary
        fields = '__all__'
        extra_kwargs = {
            'batch_no': {'read_only': True}
        }


class TestCaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('start_time'):
            start_dt = datetime.datetime.fromtimestamp(int(data.get('start_time')) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.datetime.fromtimestamp(int(data.get('end_time')) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            data['start_time'] = start_dt
            data['end_time'] = end_dt
        return data

    class Meta:
        model = TestCase
        fields = '__all__'
        extra_kwargs = {
            'batch_no': {'read_only': True}
        }


class SaveReportSerializer(serializers.Serializer):
    test_summary = TestSummarySerializer()
    test_cases = serializers.ListField(child=TestCaseSerializer(), write_only=True)

    def create(self, validated_data):
        def parse_request_data(data):
            pattern = re.compile(r'POST data:\s*(\{.*\}|.*)')
            match = pattern.search(data)

            # 如果找到匹配项，则输出POST数据
            if match:
                post_data = match.group(1)
                return post_data

            return data

        summary_data = validated_data.get('test_summary')
        cases_data = validated_data.get('test_cases')
        batch_no = generate_unique_id()

        summary = TestSummary.objects.create(batch_no=batch_no, **summary_data)
        new_cases = [{'batch_no': batch_no, **cd, 'request_body': parse_request_data(cd.get('request_body'))} for cd in
                     cases_data]
        case_models = [TestCase(**nc) for nc in new_cases]
        TestCase.objects.bulk_create(case_models)
        return summary  # {'test_summary': summary}

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        data = model_to_dict(instance)
        return data
