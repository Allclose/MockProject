import HTMLTestRunner
import json
import logging
import os
import re
import socket
import threading
import time
import requests
from django.contrib.auth.models import User
from django.contrib import auth #导入用户信息
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password   #密码加密
from django.shortcuts import render
from Myapp.models import *
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
import random
#引入发送邮件的模块
from django.core.mail import send_mail
from django.conf import settings
import shutil
#py操作shell命令
import subprocess
import unittest
import xlrd
#py操作dos命令

project_path = os.path.split(os.path.realpath(__file__))[0]
report_path = os.path.join(project_path,'templates\ApiResult')
testcase_path = os.path.join(project_path,r'common\testCase')
@login_required()
#项目列表页面
def project_list(request):
    res = {}
    if request.session['user'] == 'admin':
        res['project'] = DB_project.objects.all()
    else:
        res['project'] = DB_project.objects.filter(user=request.session['user'])
    res['buttons'] = [{"name": '新增项目', "href": 'javascript:add_project()', "icon": "folder"},
                      {"name":'项目数据',"href":'javascript:project_data()',"icon":"database"},]
    res['page_name'] = '项目列表页'
    res['user'] = request.session['user']
    return render(request,'project_list.html',res)
#新增项目及脚本
def add_project(request):
    name = request.GET['new_name']
    black_hosts = request.GET['black_hosts']
    white_hosts = request.GET['white_hosts']
    user = request.session['user']
    project = DB_project.objects.create(name=name, white_hosts=white_hosts, black_hosts=black_hosts,user=user)
    shutil.copy("Myapp/mitm_edits/mitm_edit.py", "Myapp/mitm_edits/%s_mitm_edit.py" % project.id)
    return HttpResponseRedirect('/project_list/')
#修改项目
def get_project(request,id):
    res = {}
    project = DB_project.objects.filter(id=id).values()[0]
    res['project'] = project
    return HttpResponse(json.dumps(res),content_type='application/json')
def project_set(request,id):
    project_id = id
    new_name = request.GET['new_name']
    black_hosts = request.GET['black_hosts']
    white_hosts = request.GET['white_hosts']
    DB_project.objects.filter(id=project_id).update(name=new_name,white_hosts=white_hosts,black_hosts=black_hosts)
    return HttpResponse('OK')
#项目数据
def project_data(request):
    pass
#删除项目、单元、脚本
def del_project(request,id):
    project = DB_project.objects.filter(id=id).delete()
    DB_mock.objects.filter(project_id=id).delete()
    try:
        os.remove("Myapp/mitm_edits/%s_mitm_edit.py"%id)
    except:
        pass
    return HttpResponseRedirect('/project_list/')
#登录页面
def login(request):
    return render(request,'login.html') #返回登录页面
#登录操作
def sign_in(request):
    #获取前端信息
    username = request.GET['in_username']
    password = request.GET['in_password']
    #用户表内校验
    user = auth.authenticate(username=username,password=password)
    #判断
    if user is None:
        return HttpResponseRedirect('/login')
    else:
        auth.login(request, user)
        request.session['user'] = username
        return HttpResponseRedirect('/project_list/')
        #添加登录态信息，进行实际登录
#退出
def logout(request):
    #退出用户登录态
    auth.logout(request)
    return HttpResponseRedirect('/login')
#注册
def sign_up(request):
    #获取前端信息
    username = request.GET['up_username']
    password = request.GET['up_password']
    email = request.GET['up_email']
    #注册
    try:
        #注册新增用户
        user = User.objects.create_user(username=username,password=password,email=email)
        user.save()
        # 用户直接登录
        auth.login(request,user)
        request.session['user'] = username
        return HttpResponseRedirect('/project_list/')
    #注册失败直接返回登录页面
    except:
        return HttpResponseRedirect('/login')
#重置密码，忘记密码
def reset_password(request):
    #获取前端信息
    username=request.GET['fg_username']
    code = request.GET['fg_code']
    password = request.GET['fg_password']
    #查询库内数据进行校验
    user = User.objects.filter(username=username)
    if code == user[0].last_name:
        #更新并加密密码
        user.update(password=make_password(password))
        auth.login(request,username)
        return HttpResponseRedirect('/project_list')
    else:
        return HttpResponse('验证码错误')
    #判断后处理
#发送重置密码的验证码到邮件
def send_email_pwd(request):
    #获取到用户名
    username = request.GET['username']
    #查询是否有该用户
    if User.objects.filter(username=username) == None:
        return HttpResponse('未找到该用户')
    # 查到对应存储的email地址并发送随机4位数
    # 生成随机验证码
    else:
        email = User.objects.filter(username=username)[0].email
        code = str(random.randint(1000,9999))
        #保存随机验证码用户校验    姓氏用作存储code
        User.objects.filter(username=username).update(last_name=code)
        #发送邮件
        msg='找回密码的验证码：'+code
        send_mail('找回密码',msg,settings.EMAIL_FROM,[email])
        #返回信息
        return HttpResponse('yes')
#mock单元类接口
#进入mock单元页面并返回项目下单元数据
def mock_list(request,project_id):
    #获取项目信息
    project = DB_project.objects.filter(id=project_id,user=request.session['user'])[0]
    #获取本地ip信息
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        #关闭连接
        s.close()
    #获取mock信息
    res = {}
    res['buttons'] = [{"name":'新增单元',"href":'/add_mock/%s/'%project_id,"icon":"folder"},    #传出项目id
                      {"name":'抓包导入',"href":'javascript:show_catch()',"icon":"hand-o-right"},#可通过javascript:函数名()直接调用js的函数
                      {"name":'启动服务',"href":'/server_on/%s/'%project_id,"icon":"hourglass-start"},
                      {"name":'关闭服务',"href":'/server_off/%s/'%project_id,"icon":"hourglass-end"}]
    res['mocks'] = DB_mock.objects.filter(project_id=project_id)
    res['page_name'] = '项目详情页:[%s]'%project.name +'【HOST】 : '+ ip +'  【PORT】 : '+str(9000+int(project_id))
    res['project_state'] = '  服务状态: '+str(project.state)
    res['project'] = project
    res['user'] = request.session['user']
    return render(request,'mock_list.html',res)
#新增mock单元
def add_mock(request,project_id):
    #新增mock单元
    #name = request.GET['name']
    DB_mock.objects.create(name='name',project_id=project_id)
    new_mocks_counts = DB_project.objects.filter(id=project_id)[0].mocks + 1
    DB_project.objects.filter(id=project_id).update(mocks=new_mocks_counts)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)
#设置保存 单元
def get_mock(request):
    mock_id=request.GET['mock_id']
    mock = DB_mock.objects.filter(id=mock_id).values()[0]   #将获取的变为列表,对单双引号进行转码后使用
    res = {'mock':mock}
    return HttpResponse(json.dumps(res),content_type='application/json')
def mock_set(request):
    mock_id=request.GET['mock_id']
    name = request.GET['mock_name']
    catch_url = request.GET['catch_url']
    mock_response_body = request.GET['mock_response_body']
    model = request.GET['model']
    response_headers = request.GET['response_headers']
    state_code = request.GET['state_code']
    mock_response_body_lj = request.GET['mock_response_body_lj']
    mock_time = request.GET['mock_time']
    DB_mock.objects.filter(id=mock_id).update(name=name,
                                              catch_url=catch_url,
                                              mock_response_body=mock_response_body,
                                              model=model,
                                              response_headers = response_headers,
                                              state_code = state_code,
                                              mock_response_body_lj = mock_response_body_lj,
                                              mock_time = mock_time)
    return HttpResponse('')
#删除mock单元
def del_mock(request,mock_id):
    mocks = DB_mock.objects.filter(id=mock_id)
    project_id = mocks[0].project_id
    mocks.delete()
    new_mocks_counts = DB_project.objects.filter(id=project_id)[0].mocks - 1
    DB_project.objects.filter(id=project_id).update(mocks=new_mocks_counts)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)
#启用mock单元
def mock_on(request,mock_id):
    mock = DB_mock.objects.filter(id=mock_id)
    mock.update(state=True)
    return HttpResponseRedirect('/mock_list/'+mock[0].project_id)
#弃用mock单元
def mock_off(request,mock_id):
    mock = DB_mock.objects.filter(id=mock_id)
    mock.update(state=False)
    return HttpResponseRedirect('/mock_list/%s/' % mock[0].project_id)
#服务启动
def server_on(request,project_id):
    #使用子线程去执行启动服务命令
    def thread_on():
        DB_project.objects.filter(id=project_id).update(state=True)
        port = str(9000+int(project_id))
        script = 'Myapp/mitm_edits/'+project_id+'_mitm_edit.py'
        cmd = 'mitmdump -p %s -s %s'%(port,script)
        #dos命令使用
        os.system(cmd)
        #shell命令使用
        #subprocess.call(cmd,shell=True)
    t = threading.Thread(target=thread_on)  #启动子线程
    t.start()
    return HttpResponseRedirect('/mock_list/%s/'%project_id)
#关闭服务>
def server_off(request,project_id):
    def thread_off():
        port = str(9000 + int(project_id))
        #shell命令使用
        '''cmd = 'ps -ef |grep mitm |grep %s'%port
        res = subprocess.check_output(cmd,shell=True)
        for i in str(res).split('\\n'):
            if project_id+'_mitm_edit.py' in i:
                ids = re.findall(r'\d+',i.split('/')[0])   #取命令前面部分进行正则匹配，取最大的多位数字即为pid
                pid = max([int(i) for i in ids])        #无法对字符串使用max比对，需转为int类型[int(i) for i in ids]
                subprocess.call('kill -9 %s'%str(pid), shell=True)
                break
        else:
            print('未找到进程')'''
        #dos命令使用
        try:
            cmd = 'netstat -ano |findstr %s'%port
            res = os.popen(cmd).read()              #获取端口相关进程信息
            pid = res.split('\n')[0].split('LISTENING')[1].strip()  #获取进程id
            kill_cmd = 'taskkill /T /F /PID %s' % pid
            os.system(kill_cmd)
        except:
            print('未找到进程')
    t = threading.Thread(target=thread_off)
    t.start()
    DB_project.objects.filter(id=project_id).update(state=False)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)
#获取抓包日志，每秒运行一次
def get_catch_log(request):
    project_id = request.GET['project_id']
    project = DB_project.objects.filter(id=project_id)
    project.update(catch=True)  #打开开关，启动抓包
    try:
        catch_log = eval(project[0].catch_log)  #h获取数据库内日志，并转化为原数据类型-列表
    except:
        print('catch_log格式错误')
    ret = {'res':catch_log}
    #删除原数据库内数据
    project.update(catch_log='[]',catch_time=time.time())
    return HttpResponse(json.dumps(ret,ensure_ascii=False),content_type='application/json',)
#导入所选请求记录为mock单元
def import_catch(request):
    chose_catch = json.loads(request.POST['chose_catch'])
    project_id = request.POST['project_id']
    DB_mock.objects.create(project_id=project_id,
                           name=chose_catch['url'][:500],
                           catch_url='/'+'/'.join(chose_catch['url'].split('?')[0].split('/')[3:]),
                           response_headers=chose_catch['response_headers'],
                           mock_response_body_lj=chose_catch['response_content']
                           )
    return HttpResponse('')
#接口测试页面
def api_list(request):
    res = {}
    res['apis'] = DB_api.objects.all()
    res['buttons'] = [{"name": '新增接口', "href": 'javascript:add_api()', "icon": "folder"},
                      {"name": '模板下载', "href": 'javascript:down_case_demo()', "icon": "folder"}]
    return render(request,'api_list.html',res)
#新增接口
def add_api(request):
    name = request.POST['name']
    method = request.POST['method']
    url = request.POST['url']
    body = request.POST['body']
    check = request.POST['check']
    api = DB_api.objects.create(name=name,method=method,url=url,body=body,check=check)
    api.save()
    demo_case = os.path.join(testcase_path,'test_testcase.py')
    new_case = os.path.join(testcase_path,'test_'+str(api.id)+'_testcase.py')
    shutil.copy(demo_case,new_case)
    return HttpResponse('success')
#运行接口测试
def run(request,api_id):
    #获取接口id，匹配对应用例脚本
    api_id = api_id
    #获取数据库用例并加载
    suite = unittest.TestSuite()
    suite_mode = []
    #获取用例脚本并加载对应用例
    discover = unittest.defaultTestLoader.discover(start_dir=testcase_path,pattern='test_'+api_id+'_testcase.py',top_level_dir=None)
    suite_mode.append(discover)
    if len(suite_mode) >0:
        for i in suite_mode:
            for test_name in i:
                suite.addTest(test_name)
    #执行
    report =os.path.join(report_path,str(api_id)+'_report.html')
    fp = open(report,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='测试报告')
    runner.run(suite)
    fp.close()
    return HttpResponse('')
#查看测试报告
def show_report(request,api_id):
    try:
        report = os.path.join(report_path,str(api_id)+'_report.html')
        return render(request, report)
    except:
        return HttpResponse('暂无报告')
#下载测试用例模板
def down_case_demo(request):
    pass
#接口设置
def get_api(request):
    api_id = request.GET['api_id']
    api = DB_api.objects.filter(id=api_id).values()[0]
    res = {'api':api}
    return HttpResponse(json.dumps(api),content_type='application/json')
def set_api(request):
    api_id = request.POST['api_id']
    name = request.POST['name']
    method = request.POST['method']
    url = request.POST['url']
    body = request.POST['body']
    check = request.POST['check']
    DB_api.objects.filter(id=api_id).update(name=name,method=method,url=url,body=body,check=check)
    return HttpResponse('OK')
#删除接口
def del_api(request,api_id):
    api = DB_api.objects.filter(id=api_id).delete()
    report = os.path.join(report_path,api_id+'_report.html')
    testcase = os.path.join(testcase_path,'test_'+str(api_id)+'_testcase.py')
    try:
        os.remove(testcase)
    except FileNotFoundError:
        print('未找到报告文件')
    try:
        os.remove(report)
    except FileNotFoundError:
        print('未找到报告文件')
    return HttpResponse('ok')

#测试用例
def case_list(request,api_id):
    api_id = api_id
    res = {}
    res['apis'] = DB_api.objects.filter(id=api_id)[0]
    res['cases'] = DB_case.objects.filter(api_id=api_id)
    res['buttons'] = [{"name": '导入用例', "href": '#', "icon": "folder"},
                        {"name": '新增用例', "href": "javascript:add_case()", "icon": "folder"},]
    res['user'] = request.session['user']
    return render(request,'case_list.html',res)
#新增用例
def add_case(request,api_id):
    excel_data = request.FILES['excel_data']    #获取到用例名称
    cases = xlrd.open_workbook(filename=None, file_contents=excel_data.read()) #需要使用read()进行读取
    table = cases.sheets()[0]
    row = table.nrows
    cases = []
    try:
        if row >1:
            for i in range(1, row):     #首行为表头
                col = table.row_values(i)       #用例行：['login', '/login', 'name=xiaoming&pwd=111', 200.0]
                cases.append(col)
    except:
        return HttpResponse('文件读取失败')
    api = DB_api.objects.filter(id=api_id).update(testcases=str(cases))
    return HttpResponseRedirect('/api_list/')
def set_case(request):
    pass