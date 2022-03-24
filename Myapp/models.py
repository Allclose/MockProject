from django.db import models

# Create your models here.
class DB_project(models.Model):
    name = models.CharField(max_length=30,null=False,blank=False)
    user = models.CharField(max_length=30,null=True,blank=True)
    mocks = models.IntegerField(default=0)
    run_counts = models.IntegerField(default=0)
    mock_counts = models.IntegerField(default=0)
    state = models.BooleanField(default=False)
    catch_log = models.TextField(default='[]')      #保存抓包日志
    catch = models.BooleanField(default=False)      #在线抓包开关
    white_hosts = models.CharField(max_length=500,null=True,blank=True,default='')   #白名单，不为空则只抓白名单内的
    black_hosts = models.CharField(max_length=500,null=True,blank=True,default='')   #抓包黑名单
    catch_time = models.CharField(max_length=20,null=True,blank=True,default='')        #最后一次在线抓包的时间
    def __str__(self):
        return self.name
class DB_mock(models.Model):
    name = models.CharField(max_length=30,null=False,blank=False)
    state = models.BooleanField(default=True)
    project_id = models.CharField(max_length=30,null=True,blank=True)
    catch_url = models.CharField(max_length=500,null=True,blank=True,default=' ')
    model = models.TextField(null=True,blank=True,default='fx',max_length=30)   #fx是放行模式，lj是拦截模式
    state_code = models.IntegerField(default=200)
    response_headers = models.CharField(max_length=500,null=True,blank=True,default='{}')
    mock_response_body = models.TextField(null=True,blank=True,default='')
    mock_response_body_lj = models.TextField(null=True,blank=True,default='')   #拦截模式的写死的返回值
    mock_time = models.FloatField(default=0)            #响应时间控制
    def __str__(self):
        return self.name
class DB_api(models.Model):
    name = models.CharField(max_length=200,null=True,blank=False,default='')
    url = models.CharField(max_length=200,null=True,blank=False,default='')
    method = models.CharField(max_length=200,null=True,blank=False,default='get')
    body = models.CharField(max_length=200, null=True, blank=False,default='')
    check = models.CharField(max_length=200, null=True, blank=False,default=200)
    testcases = models.TextField(null=True,blank=True,default='')
    def __str__(self):
        return self.name
class DB_case(models.Model):
    api_id = models.CharField(max_length=20,null=True,blank=False)
    name = models.CharField(max_length=200,null=True,blank=False)
    body = models.CharField(max_length=500,null=True,blank=False)
    check = models.CharField(max_length=500,null=True,blank=False)
    def __str__(self):
        return self.name