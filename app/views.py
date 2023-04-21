# Create your views here.
from django.db.models import Q
from rest_framework import views
from common.response import Response

from app.models import TestSummary, TestCase
from app.serializer import TestSummarySerializer, TestCaseSerializer, SaveReportSerializer
from app.validator import ChartDataSerializer, SummaryFilterSerializer, LatestBuildSerializer
from common.utils import transition_time


class SaveResultsView(views.APIView):
    """
        保存测试结果: 仅在JMeter后端监视器内部使用
    """

    def post(self, request):
        serializer_data = SaveReportSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
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
    图表趋势数据
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
    """
    构建测试记录
    """

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
        else:
            return Response(data=req.errors)


class SummaryDetailView(views.APIView):
    """
    测试详情
    """

    def get(self, request, pk):
        summary_info = TestSummary.objects.get(pk=pk)
        cases_info = TestCase.objects.filter(batch_no=summary_info.batch_no)

        summary_serializer = TestSummarySerializer(instance=summary_info).data
        cases_serializer = TestCaseSerializer(instance=cases_info, many=True).data

        return Response(data={'summary_info': summary_serializer, 'case_info': cases_serializer})


class BaseInfoView(views.APIView):
    """
    项目环境信息
    """

    def get(self, request):
        project = TestSummary.objects.values_list('project', flat=True).distinct()
        env = TestSummary.objects.values_list('env', flat=True).distinct()
        data = {'project': project, 'env': env}
        return Response(data=data)


class TestView(views.APIView):
    """
    测试接口
    """

    def get(self, reqeust):
        return Response(data=reqeust.query_params)

    def post(self, reqeust):
        return Response(data=reqeust.data)
