#非项目内文件获取项目内数据库时需引入django
import sys
import django
import os
sys.path.append("E:\Test\AppMock")
os.environ.setdefault("DJANGO_SETTINGS_MODULE","AppMock.settings")
django.setup()
import http
from Myapp.models import *
import json

def request(flow):
    #对请求发送到服务器之前进行干预的脚本
    pass
def response(flow):
    #在请求从服务器返回后进行干预的脚本
    project_id = os.path.basename(__file__).split('_')[0]
    mocks = DB_mock.objects.filter(project_id=project_id,state=True)
    for mock in mocks:
        if mock.catch_url  in flow.request.url:
            #获取数据库内的更新策略，并切片分条
            updates = mock.mock_response_body.split('\n')
            for i in updates:
                if '=>' in i:
                    #不对响应信息进行unicode编码，保证中文类型状态，以确保策略key可以捕捉到
                    try:
                        json.loads(flow.response.text)  #替换为字典，可以显示为中文，但字典不合下方替换规则
                        #转换为字典后再转换为json字符，但不予进行转码-ensure_ascii=False
                        flow.response.text = json.dumps(json.loads(flow.response.text),ensure_ascii=False)
                    except:
                        ...
                    flow.response.text = flow.response.text.replace(i.split('=>')[0].strip(),i.split('=>')[1].strip())
                #json路径格式更新规则
                elif '=' in i:
                    #获取响应原信息
                    try:
                        old = json.loads(flow.response.text)    #转换为字典
                    except:
                        continue
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
                    flow.response.text = json.dumps(old)    #转换为json字符串返回给前端
                else:
                    continue
            break   #确保一次只中一次mock单元