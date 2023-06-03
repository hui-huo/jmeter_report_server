from django.db import models

# Create your models here.
from django.utils import timezone


class TestSummary(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.CharField(max_length=200, unique=True, verbose_name="用例批次编号")
    project = models.TextField(verbose_name="项目名称")
    env = models.TextField(verbose_name="环境名称")
    type = models.SmallIntegerField(verbose_name="构建类型")
    scenario = models.TextField(default=0, verbose_name="场景数")
    total = models.IntegerField(verbose_name="用例数")
    success = models.IntegerField(verbose_name="成功数")
    fail = models.IntegerField(verbose_name="失败数")
    pass_rate = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="通过率")
    duration = models.IntegerField(verbose_name="持续时间")
    result = models.BooleanField(verbose_name="测试结果")
    start_time = models.BigIntegerField(verbose_name="测试开始时间")
    end_time = models.BigIntegerField(verbose_name="测试结束时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    last_updated = models.DateTimeField(default=timezone.now, verbose_name="更新时间")

    class Meta:
        verbose_name = '测试概括'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.batch_no


class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.CharField(max_length=200, verbose_name="批次编号")
    module_name = models.TextField(default="-", verbose_name="模块名称")
    scenario_name = models.TextField(default="-", verbose_name="场景名称")
    case_name = models.TextField(verbose_name="用例名称")
    request_url = models.TextField(verbose_name="请求地址")
    request_method = models.TextField(blank=True, null=True, verbose_name="请求方法")
    request_header = models.TextField(blank=True, null=True, verbose_name="请求头")
    request_body = models.TextField(blank=True, null=True, verbose_name="请求体")
    response_header = models.TextField(blank=True, null=True, verbose_name="响应头")
    response_body = models.TextField(blank=True, null=True, verbose_name="响应体")
    response_code = models.TextField(blank=True, null=True, verbose_name="响应状态码")
    success = models.BooleanField(default=False, verbose_name="测试结果")
    fail_message = models.TextField(blank=True, null=True, verbose_name="失败信息")
    start_time = models.BigIntegerField(verbose_name="开始时间")
    end_time = models.BigIntegerField(verbose_name="结束时间")

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.case_name
