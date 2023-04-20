from django.db import models


# Create your models here.

class TestSummary(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.CharField(max_length=50, unique=True, verbose_name="用例批次编号")
    project = models.CharField(max_length=50, verbose_name="项目名称")
    env = models.CharField(max_length=50, verbose_name="环境名称")
    type = models.SmallIntegerField(verbose_name="构建类型")
    total = models.IntegerField(verbose_name="用例总数")
    success = models.IntegerField(verbose_name="成功总数")
    fail = models.IntegerField(verbose_name="失败总数")
    pass_rate = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="通过率")
    duration = models.IntegerField(verbose_name="持续时间")
    result = models.BooleanField(verbose_name="测试结果")
    start_time = models.BigIntegerField(max_length=50, verbose_name="开始时间")
    end_time = models.BigIntegerField(max_length=50, verbose_name="结束时间")

    class Meta:
        verbose_name = '测试概括'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.batch_no


class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.CharField(max_length=50, verbose_name="批次编号")
    module_name = models.CharField(max_length=50, verbose_name="模块名称")
    case_name = models.CharField(max_length=50, verbose_name="用例名称")
    request_url = models.CharField(max_length=50, verbose_name="请求地址")
    request_method = models.TextField(blank=True, null=True, verbose_name="请求方法")
    request_header = models.TextField(blank=True, null=True, verbose_name="请求头")
    request_body = models.TextField(blank=True, null=True, verbose_name="请求体")
    response_header = models.TextField(blank=True, null=True, verbose_name="响应头")
    response_body = models.TextField(blank=True, null=True, verbose_name="响应体")
    response_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="响应状态码")
    test_result = models.BooleanField(verbose_name="测试结果")
    fail_message = models.TextField(blank=True, null=True, verbose_name="模块名称")
    start_time = models.BigIntegerField(verbose_name="开始时间")
    end_time = models.BigIntegerField(verbose_name="结束时间")

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.case_name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="图书名称", help_text="图书名称")
    isbn = models.CharField(max_length=50, help_text="图书编号")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        return 100
