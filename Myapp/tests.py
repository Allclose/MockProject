
# Create your tests here.
import re

import requests,json,os,os.path,sys
import unittest


class dep_auto(unittest.TestCase):
    headers = {"Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Cookie": "UUMS=7242534c-762f-47f4-88d9-e6287872fa03; schedulerToken=feb1a4e73416e05948bde646e9c01273; PROJECTID=10",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
    body = json.dumps({"scriptName": "4.py",
                  "scriptType": "PYTHON",
                  "ddTreeId": 44,
                  "type": "add",
                  "hasEdit": "false",
                  "newTitle": "4.py",
                  "content": "",
                  "projId": 10,
                  "scriptParams": []
                })
    Cookie = "UUMS=7242534c-762f-47f4-88d9-e6287872fa03; schedulerToken=feb1a4e73416e05948bde646e9c01273; PROJECTID=10"
    param = {}

    def test_2_search(self):
        url = r'http://172.20.81.17:8001/api/dep-data-dev/dataDevScript/scriptNodes?ddTreeId=44'
        response = json.loads(requests.get(url=url,headers=self.headers).text)
        r = r"scriptId': (.*?), 'remark"
        result = re.findall(r,str(response['data']))
        self.assertEqual(response['status'],200)
        return result[-1]
    def test_1_add(self):
        response = json.loads(requests.post(url=r'http://172.20.81.17:8001/api/dep-data-dev/dataDevScript',
                                 data=self.body,
                                 headers=self.headers).text)
        self.param['scriptId'] = response['data']['scriptId']
        #return response['status']       #{'status': 200, 'message': '操作成功', 'data': {'scriptId': 357, 'parentDdTreeIds': '0'}}
        self.assertEqual(str(response['data']['scriptId']),self.test_2_search(),'失败')
#dep_auto().test_1_add()
if '__name__' == '__main__':
    unittest.main(verbosity=2)
    ...
