"""jmeter_report_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app.views import SaveResultsView, LatestBuildView, CharDataView, SummaryListView, BaseInfoView, \
    SummaryDetailView, DeleteSummary, TestView

urlpatterns = [
    path('result/save', SaveResultsView.as_view(), name='保存报告'),
    path('result/latest', LatestBuildView.as_view(), name='最新构建'),
    path('chart/data', CharDataView.as_view(), name='图表数据'),
    path('summary/list', SummaryListView.as_view(), name='报告列表'),
    path('summary/delete', DeleteSummary.as_view(), name='报告删除'),
    path('case/detail/<int:pk>', SummaryDetailView.as_view(), name='用例信息'),
    path('project/info', BaseInfoView.as_view(), name='项目信息统计'),

    path('test', TestView.as_view(), name='项目信息统计'),
]
