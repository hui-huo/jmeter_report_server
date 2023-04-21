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
from django.contrib import admin
from django.urls import path

from app.views import SaveResultsView, LatestBuildView, CharDataView, SummaryListView, BaseInfoView, \
    SummaryDetailView, TestView

urlpatterns = [
    path('save_results', SaveResultsView.as_view(), name='保存报告'),
    path('latest_build', LatestBuildView.as_view(), name='最新构建'),
    path('chart_data', CharDataView.as_view(), name='图表数据'),
    path('summary_list', SummaryListView.as_view(), name='概括列表'),
    path('case_detail/<int:pk>', SummaryDetailView.as_view(), name='用例信息'),
    path('base_info', BaseInfoView.as_view(), name='项目信息统计'),

    path('test', TestView.as_view(), name='项目信息统计'),
]
