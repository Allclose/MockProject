#dep登录测试用例脚本
import unittest,json,os

import django
import urllib
from Myapp.common import configHttp
import requests,os
import HTMLTestRunner
import time
import paramunittest
from Myapp.models import *
django.setup()

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    "Cookie": "schedulerToken=feb1a4e73416e05948bde646e9c01273; UUMS=f42ac75e-d07a-42f3-b80c-28108f4f21ca"
    }
#result_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],'ApiResult')    #报告位置

api_id = int(os.path.basename(__file__).split('_')[1])
#excel  = readExcel.readExcel().get_xls('userCase.xlsx', 'login')
excel = eval(DB_api.objects.filter(id=api_id)[0].testcases)
@paramunittest.parametrized(*excel)   #参数化后可以单用例函数自行循环取用例进行执行
class test_login(unittest.TestCase):
    def setParameters(self, case_name, path, body, check):
        self.case_name = str(case_name)
        self.path = str(path)
        self.body = str(body)
        self.check = int(check)
    def test_01(self):
        self.checkResult()
    def checkResult(self):
        url = DB_api.objects.filter(id=api_id)[0].url
        method = DB_api.objects.filter(id=api_id)[0].method
        body = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.body).query))#将a=b转化为{"a":"b"}
        result = configHttp.RunMain().run_main(method, url,body)
        res = json.loads(result)
        self.assertEqual(res['code'],self.check,'失败')

if __name__ == '__main__':
    unittest.main(verbosity=2)
    '''suite = unittest.TestSuite()
    #suite.addTest(test_login('test_01'))
    suite.addTests(map(test_login,['test_01']))
    #运行和报告
    time = time.strftime('%Y_%m_%d_%H_%M_%S')
    st = result_path+str(time)+'.html'
    fp =  open(st,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='测试报告',description='情况',verbosity=2)
    runner.run(suite)
    fp.close()'''