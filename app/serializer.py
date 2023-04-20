# _*_ coding: utf-8 _*_
"""
Time:     2023/3/31 11:33
Author:   Hui Huo.
File:     serializer.py
Describe: 
"""

import datetime
import re

from django.db.models import Q
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import TestSummary, TestCase, Book
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
    # test_cases = TestCaseSerializer(many=True)
    test_cases = serializers.ListField(child=TestCaseSerializer(), write_only=True)

    def create(self, validated_data):
        """
            create 方法返回instance中必须包含序列化定义的字段，可以使用write_only排除
        """

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

    # 这个重写应该也可以解决自定义instance，但是走不了嵌套子类的序列化了，比如这里的summary 时间格式化没有生效
    def to_representation(self, instance):
        """
            修改序列化的数据，在第一次调用.data时调用
        """
        data = model_to_dict(instance)
        return data


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


class BookSerializer(serializers.Serializer):
    name = serializers.CharField()
    isbn = serializers.CharField()

    price = serializers.CharField(read_only=True)  # model中设置 有效

    def update(self, instance, validated_data):
        """
            更新操作，在save方法调用时 如果序列化对象有instance时调用
        """
        print(f'update...{validated_data}')
        instance.name = validated_data.get('name')
        instance.isbn = validated_data.get('isbn')
        instance.save()
        return instance

    def create(self, validated_data):
        """
            更新操作，在save方法调用时 如果序列化对象只有data时调用
        """
        print(f'create...{validated_data}')
        return Book.objects.create(**validated_data)

    def to_representation(self, instance):
        """
            修改序列化的数据，在第一次调用.data时调用
        """
        data = super().to_representation(instance)
        data['name'] = 'Python从入门到精通'
        return data

    def to_internal_value(self, data):
        """
            修改反序列化的数据，在调用is_valid()时自动调用
        """
        data['name'] = 'PHP从入门到精通'
        return super().to_internal_value(data)


class BookModelSerializer(DynamicFieldsModelSerializer):
    # price = serializers.CharField(read_only=True) # model中设置 无效
    # price = serializers.SerializerMethodField(read_only=True)  # 设置同样 无效
    # 以上两种 没有属性覆盖自动生成重写一说，只能是别名如 new_price
    #
    # def get_price(self, obj):
    #     return 100

    new_price = serializers.SerializerMethodField()  # 只能在序列化时使用，且不会对反序列化数据校验这一项, read_only的参数都不校验

    def get_new_price(self, obj):
        return 'new_100'

    # def validate(self, attrs):
    #     price = attrs.get('isbn')
    #     if isinstance(price, int):
    #         raise ValidationError('isbn必须为str类型.')
    #     else:
    #         return attrs

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'isbn': {'required': False},
            'price': {'read_only': True}  # 这种方式有效，结合到model中的property属性
        }

    # def to_internal_value(self, data):
    #     data['name'] = '红楼梦'
    #     return super().to_internal_value(data)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['name'] = '水浒传'
    #     return data
