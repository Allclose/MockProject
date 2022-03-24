#非项目内文件获取项目内数据库时需引入django
import sys
import time
import threading
import django
import os
sys.path.append("E:\Test\AppMock")
os.environ.setdefault("DJANGO_SETTINGS_MODULE","AppMock.settings")
django.setup()
from mitmproxy import http
from Myapp.models import *
import json

#黑白名单设置
def filter(flow):
    project_id = os.path.basename(__file__).split('_')[0]
    project = DB_project.objects.filter(id=project_id)[0]
    if project.white_hosts != '':
        if flow.request.url not in project.white_hosts.split(','):
            return False
    elif project.black_hosts != '':
        if flow.request.url in project.black_hosts.split(','):
            return False

#写入日志
def wrirte_catch_log(flow):
    project_id = os.path.basename(__file__).split('_')[0]
    project = DB_project.objects.filter(id=project_id)
    #读取开关，是否抓包
    catch = project[0].catch
    if catch == True:
        old_log = eval(project[0].catch_log)
        #信息头为字典
        tmp_header = {}
        for k,v in flow.response.headers.items():
            tmp_header[k]=v
        tmp_log = {
            "method":flow.request.method,
            "url":flow.request.url,
            "response_headers":json.dumps(tmp_header),
            "response_content":flow.response.text
        }
        #追加到原日志中
        old_log.append(tmp_log)
        DB_project.objects.update(catch_log=str(old_log))

#抓包
def request(flow):
    #url过滤
    if filter(flow) == False:
        return
    #拦截模式：对请求发送到服务器之前进行干预的脚本
    project_id = os.path.basename(__file__).split('_')[0]
    mocks = DB_mock.objects.filter(project_id=project_id,state=True)
    for mock in mocks:
        if mock.catch_url in flow.request.url:
            if mock.model == 'lj':
                flow.response = http.HTTPResponse.make(
                    mock.state_code,
                    mock.mock_response_body_lj,
                    json.loads(mock.response_headers)
                )
            break

def response(flow):
    # url过滤
    if filter(flow) == False:
        return
    #放行模式：在请求从服务器返回后进行干预的脚本
    project_id = os.path.basename(__file__).split('_')[0]
    mocks = DB_mock.objects.filter(project_id=project_id,state=True)
    for mock in mocks:
        if mock.catch_url  in flow.request.url:
            if mock.model == 'fx':
                #获取数据库内的更新策略，并切片分条
                updates = mock.mock_response_body.split('\n')
                for i in updates:
                    if '=>' in i:
                        # 不对响应信息进行unicode编码，保证中文类型状态，以确保策略key可以捕捉到
                        try:
                            json.loads(flow.response.text)  # 替换为字典，可以显示为中文，但字典不合下方替换规则
                            # 转换为字典后再转换为json字符，但不予进行转码-ensure_ascii=False
                            flow.response.text = json.dumps(json.loads(flow.response.text), ensure_ascii=False)
                        except:
                            ...
                        flow.response.text = flow.response.text.replace(i.split('=>')[0].strip(), i.split('=>')[1].strip())
                    #json格式更新规则
                    elif '=' in i:
                        #获取响应原信息
                        old = json.loads(flow.response.text)
                        #分离更新策略的前后key和value
                        key = i.split('=')[0].strip()
                        value = eval(i.split('=')[1].strip())
                        #将key的路径切割识别后拼接成一个字符串类型的代码，然后使用exec进行执行，获取到具体的key位置
                        tmp_cmd = ''
                        for i in key.split('.'):
                            try:
                                int(i)
                                tmp_cmd += '[%s]' %i
                            except:
                                tmp_cmd += '[%s]'%repr(i)
                        end_cmd = 'old'+tmp_cmd+'=value'
                        try:
                            exec(end_cmd)
                        except:
                            continue
                        #替换响应信息并转为json格式
                        flow.response.text = json.dumps(old)
                    else:
                        continue
                #更新返回头
                for key,value in json.loads(mock.response_headers).items():
                    flow.response.headers[str(key)] = str(value)
            #响应时间控制
            try:
                mock_time = float(mock.mock_time)
            except:
                mock_time = 0
            passtime = float(time.time()) - float(flow.request.timestamp_start)
            if mock_time > passtime:
                cha = mock_time - passtime
                time.sleep(cha)
            break

    #子线程，抓包log写入数据库
    def thread():
        t = threading.Thread(target=wrirte_catch_log,args=[flow,])
        t.setDaemon(True)   #守护线程，主线程关闭则子线程关闭
        t.start()