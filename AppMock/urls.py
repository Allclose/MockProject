"""AppMock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from Myapp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('project_list/',project_list), #进入首页
    path('',project_list),
    path('add_project/',add_project),    #新增项目
    re_path('get_project/(?P<id>.+)/',get_project), #获取项目信息
    re_path('project_set/(?P<id>.+)/',project_set), #修改项目
    path('project_data/',project_data), #获取所有项目数据
    re_path('del_project/(?P<id>.+)/',del_project),  #删除项目
    path('login/',login),   #打开登录页面
    path('accounts/login/',login), #当直接通过url进入无登录态页面时，直接跳转到登录页面
    path('sign_in/',sign_in),   #登录
    path('logout/',logout),     #退出
    path('sign_up/',sign_up),    #注册
    path('reset_password/',reset_password),   #忘记密码
    path('send_email_pwd/',send_email_pwd), #忘记密码时发送验证码
    #mock单元类路径
    re_path('mock_list/(?P<project_id>.+)/',mock_list),#进入项目对应的mock单元页面
    re_path('add_mock/(?P<project_id>.+)/',add_mock),       #新增mock单元
    re_path('mock_on/(?P<mock_id>.+)/',mock_on),        #启用单元
    re_path('mock_off/(?P<mock_id>.+)/',mock_off),       #弃用单元
    path('get_mock/',get_mock), #单元设置,
    path('mock_set/',mock_set), #单元设置,
    re_path('del_mock/(?P<mock_id>.+)/',del_mock),       #删除mock单元
    re_path('server_on/(?P<project_id>.+)/',server_on),     #项目服务启动
    re_path('server_off/(?P<project_id>.+)/',server_off),   #项目服务关闭
    path('get_catch_log/',get_catch_log),                   #获取抓包日志,
    path('import_catch/',import_catch),                     #抓包导入所选请求3
    #接口测试
    path('api_list/',api_list),     #接口列表页面
    re_path('run/(?P<api_id>.+)/',run),     #运行接口测试
    path('add_api/',add_api),               #新增接口
    re_path('show_report/(?P<api_id>.+)/',show_report), #查看测试报告
    path('get_api/',get_api),       #获取接口信息
    path('set_api/',set_api),        #接口设置
    re_path('del_api/(?P<api_id>.*)/',del_api),     #删除接口
    re_path('case_list/(?P<api_id>.+)/',case_list),     #查看用例
    re_path('add_case/(?P<api_id>.+)/',add_case),     #新增用例
]