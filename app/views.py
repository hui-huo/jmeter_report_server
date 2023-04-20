# Create your views here.
import os
import tempfile

from django.core import serializers
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from common.filter import JSONFilterBackend
from common.response import Response

from app.models import TestSummary, TestCase, Book
from app.serializer import TestSummarySerializer, TestCaseSerializer, ChartDataSerializer, BookModelSerializer, \
    SaveReportSerializer, SummaryFilterSerializer, SummaryDetailSerializer, LatestBuildSerializer
from common.exception import ChartTypeError
from common.pagination import CommonPageNumberPagination
from common.utils import generate_unique_id, transition_time


class SaveResultsView(views.APIView):
    """
        保存测试结果: 仅在JMeter后端监视器内部使用
    """

    def post(self, request):
        serializer_data = SaveReportSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            # batch_no = generate_unique_id()
            # summary_data = serializer_data.validated_data.get('test_summary')
            # cases_data = serializer_data.validated_data.get('test_cases')
            #
            # summary = TestSummary.objects.create(batch_no=batch_no, **summary_data)
            # new_cases = [{'batch_no': batch_no, **cd} for cd in cases_data]
            # case_models = [TestCase(**nc) for nc in new_cases]
            # TestCase.objects.bulk_create(case_models)
            #
            # res = TestSummarySerializer(instance=summary).data
            return Response(data=serializer_data.data)
        else:
            return Response(data=serializer_data.errors)


class LatestBuildView(views.APIView):
    """
    最新构建信息
    """

    def post(self, request):
        req = LatestBuildSerializer(data=request.data)

        if req.is_valid():
            q = Q()
            summary_all = TestSummary.objects
            if project := req.validated_data.get('project'):
                q = q & Q(project__contains=project)
            if env := req.validated_data.get('env'):
                q = q & Q(env__contains=env)

            summary_all = summary_all.filter(q).order_by('-id')
            latest_summary = summary_all[0] if summary_all else summary_all
            res_data = TestSummarySerializer(instance=latest_summary)

            return Response(data=res_data.data)
        else:
            return Response(data=req.errors)


class CharDataView(views.APIView):
    """
    图表数据
    """

    def post(self, request):
        req = ChartDataSerializer(data=request.data)
        if req.is_valid():
            q = Q()
            summary_all = TestSummary.objects

            if project := req.validated_data.get('project'):
                q = q & (Q(project__contains=project))
            if env := req.validated_data.get('env'):
                q = q & (Q(env__contains=env))
            if start_time := req.validated_data.get('start_time'):
                q = q & (Q(start_time__gte=start_time))
            if end_time := req.validated_data.get('end_time'):
                q = q & (Q(end_time__lte=end_time))

            records = summary_all.filter(q).order_by('-id')
            data_list = []

            chart_type = req.validated_data.get("type")
            if chart_type == '0':
                for record in records:
                    data_list.append(
                        {'id': record.id, 'batch_no': record.batch_no, 'type': 'success', 'value': record.success})
                    data_list.append(
                        {'id': record.id, 'batch_no': record.batch_no, 'type': 'fail', 'value': record.fail})
                return Response(data=data_list)
            if chart_type == '1':
                for record in records:
                    data_list.append(
                        {'id': record.id, 'batch_no': record.batch_no, 'pass_rate': record.pass_rate})
                return Response(data=data_list)
            return Response(data=data_list)
        else:
            return Response(data=req.errors)


class SummaryListView(views.APIView):

    def post(self, request):
        req = SummaryFilterSerializer(data=request.data)
        if req.is_valid():
            q = Q()
            summary_all = TestSummary.objects.all()

            if project := req.validated_data.get('project'):
                q = q & Q(project__contains=project.strip())
            if env := req.validated_data.get('env'):
                q = q & Q(env__contains=env.strip())
            if _type := req.validated_data.get('type'):
                q = q & Q(type__contains=_type.strip())
            if result := req.validated_data.get('result'):
                res = int(result)
                q = q & Q(result__exact=res)
            if start := req.validated_data.get('start_time'):
                q = q & Q(start_time__gt=transition_time(start))
            if end := req.validated_data.get('end_time'):
                q = q & Q(end_time__lt=transition_time(end))
            if pass_rate := req.validated_data.get('pass_rate'):
                order = ('pass_rate', '-id') if pass_rate == 'ascend' else ('-pass_rate', '-id')
                query_result = summary_all.filter(q).order_by(*order)
            else:
                query_result = summary_all.filter(q).order_by('-id')

            res_data = TestSummarySerializer(instance=query_result, many=True)
            return Response(data=res_data.data)

            # {"pass_rate": "2312"}

            # req.validated_data.get('result')
            # if (result := req.validated_data.get('result')) is not None:
            #     q = q & Q(result=result)
            #
            # pagination = CommonPageNumberPagination()
            # pagination.page_size = req.validated_data.get('size')
            # pagination.page = req.validated_data.get('page')
            #
            # paginate_queryset = pagination.paginate_queryset(summary_all.filter(q).order_by('-id'), request)
            # res_data = TestSummarySerializer(instance=paginate_queryset, many=True)
            # return pagination.get_paginated_response(res_data.data)
        else:
            return Response(data=req.errors)


class SummaryDetailView(views.APIView):

    def get(self, request, pk):
        summary_info = TestSummary.objects.get(pk=pk)
        cases_info = TestCase.objects.filter(batch_no=summary_info.batch_no)

        summary_serializer = TestSummarySerializer(instance=summary_info).data
        cases_serializer = TestCaseSerializer(instance=cases_info, many=True).data

        return Response(data={'summary_info': summary_serializer, 'case_info': cases_serializer})


class BaseInfoView(views.APIView):

    def get(self, request):
        project = TestSummary.objects.values_list('project', flat=True).distinct()
        env = TestSummary.objects.values_list('env', flat=True).distinct()
        data = {'project': project, 'env': env}
        return Response(data=data)


# class SummaryListView(GenericAPIView):
# queryset = TestSummary.objects
# serializer_class = TestSummarySerializer
# filter_backends = [JSONFilterBackend, OrderingFilter]
# filterset_fields = ['name', 'isbn']
# ordering_fields = ['id']
#
# pagination_class = CommonPageNumberPagination
#
# def post(self, requests):
#     summary_list = self.get_serializer(instance=self.paginate_queryset(self.filter_queryset(self.get_queryset())),
#                                        fields=('id', 'batch_no', 'project'),
#                                        many=True)
#     return summary_list

class GenericView(GenericAPIView):
    # lookup_field = 'name'         # 默认pk=id，get_object()关联此值
    queryset = Book.objects
    serializer_class = BookModelSerializer

    # filter_backends = [SearchFilter]  # 内置过滤器，固定写法
    # search_fields = ('name',)  # /api/v1/books?search=红，name或price中只要有红就会搜出来

    filter_backends = [DjangoFilterBackend, OrderingFilter]  # 第三方过滤器
    filterset_fields = ['name', 'isbn']
    ordering_fields = ['id']

    pagination_class = CommonPageNumberPagination

    def get(self, request, pk=None):
        if pk is None:
            serializer = self.get_serializer(instance=self.paginate_queryset(self.filter_queryset(self.get_queryset())),
                                             fields=('name', 'isbn'),
                                             many=True)  # 必须套在原来的查询上分页和筛选信息
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(instance=self.get_object())
            return Response(serializer.data)

    def post(self, request):
        serializer_data = self.get_serializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(msg=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        serializer_data = self.get_serializer(data=request.data, instance=self.get_object())

        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object()
        obj.delete()
        return Response({'msg': '删除成功'})

# class BookView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = Book.objects
#     serializer_class = BookModelSerializer
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#
# class BookDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = Book.objects
#     serializer_class = BookModelSerializer
#
#     def get(self, request, pk):
#         return self.retrieve(request)
#
#     def put(self, request, pk):
#         return self.update(request)
#
#     def delete(self, request, pk):
#         return self.destroy(request)

# @csrf_exempt
# def upload(request):
#     import xmind
#     if request.method == 'POST':
#         xmind_file = request.FILES.get('xmind')
#         # 临时文件
#         with tempfile.NamedTemporaryFile(suffix='.xmind', delete=False) as tmp:
#             for chunk in xmind_file.chunks():
#                 tmp.write(chunk)
#             tmp_path = tmp.name
#         # 读取文件
#         workbook = xmind.load(tmp_path)
#         # 删除文件
#         os.unlink(tmp_path)
#         # 数据获取
#         if workbook.getData():
#             case_len = len(workbook.getData()[0].get('topic').get('topics'))
#             return JsonResponse({'case_count': case_len})
#         return JsonResponse({'case_count': 0})
#     return JsonResponse({'msg': 'upload.html'})
