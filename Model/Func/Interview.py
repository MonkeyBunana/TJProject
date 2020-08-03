# -*- coding: utf-8 -*-
import random
import json
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage

class InterviewPage:

    def __init__(self):
        self.rp = RequestsPage()
        self.ep = ElibPage('zhonglilong', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D')

    def subscriptionBooksImport(self):
        # TODO 上传文件传值不正确
        return self.rp.sendRequest('FILE', self.ep.getUrl() + '/service/api/e/interview/file/zdsmI', {
            'Content-Disposition: form-data; name="%s"; filename="%s" Content-Type:%s\r\n' % ('excel', 'list.xls', 'application/vnd.ms-excel'): 'file',
            'Content-Disposition: form-data;name="%s"' % 'userToken': self.ep.getUserToken()
        })

    def subscriptionBooks(self):
        # TODO 流程复杂，稍后实现
        # 先在 预订单管理 设置第一个为工作预定单
        self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.ep.getUserToken(),
            'ydpcid': self.ep.getYdd()[0]
        })

    def directSubscription(self):
        # 先在 预订单管理 设置第一个为工作预定单
        self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.ep.getUserToken(),
            'ydpcid': self.ep.getYdd()[0]
        })
        # 获取图书信息
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/yd/searchBook', {
            'userToken': self.ep.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'flag': 1
        }).json()
        # 征订书目-直接预订
        r = self.ep.getZdsmReserve(res['data']['dataList'][0]['marcid'])
        # 预定
        result = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/yd/smSave', {
            'userToken': self.ep.getUserToken(),
            'cygName': r['data']['cygName'],
            'ysName': r['data']['ysName'],
            'marcid': r['data']['marcid'],
            'gysName': r['data']['gysName'],
            'ydbhao': '',
            'ydpcid': r['data']['ydpcid'],
            'ceshu': 1,
            'ydlaiyuan': '订购',
            'yjhbid': self.ep.getHbList('CNY'),
            'jzleixing': '纸张',
            'yuanjia': 0,
            'zdfangshi': '平装',
            'ydhbid': self.ep.getHbList('CNY'),
            'juance': 1,
            'jiage': 0,
            'fuzhu': '',
            'ydpcdm': 1,
            'ysCode': r['data']['ysCode'],
            'gysCode': r['data']['gysCode'],
            'ydleixing': '直接预订'
        }).json()
        return result['message']  # 操作成功!  已超出预算金额，不能预订！

    def subscriptionVerify(self):
        # 先在 验收单管理 设置第一个为工作验收单
        self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.ep.getUserToken(),
            'yspcid': self.ep.getYsd()[0]
        })
        # 获取图书信息
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/yd/smSearch', {
            'userToken': self.ep.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'from': 1,
            'flag': 1
        }).json()
        # 获取索书号
        r = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/ys/curSshao', {
            'userToken': self.ep.getUserToken(),
            'marcid': res['data']['dataList'][0]['marcid']
        }).json()
        # 验收
        numList = list()
        for i in range(res['data']['dataList'][0]['ceshu']):
            numDict = dict()
            numDict['barcode'] = "TS" + str(random.randint(1, 10000)).zfill(5)
            numDict['libId'] = self.ep.getLibid()
            numDict['czId'] = self.ep.getCzid()[0]
            numDict['ltlxId'] = self.ep.getLtlxid()
            numList.append(numDict)
        # '['
        #     '{"barcode": "test100", "libId": "2", "czId": "ebd840b69bc04948859cd05a4da638b3", "ltlxId": "1"},'
        #     '{"barcode": "test101", "libId": "2", "czId": "ebd840b69bc04948859cd05a4da638b3", "ltlxId": "1"}'
        # ']',

        result = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/interview/ys/smSave', {
            'userToken': self.ep.getUserToken(),
            'marcid': res['data']['dataList'][0]['marcid'],
            'yslxing': '预订验收',
            'yspcid': self.ep.getYsd()[0],
            'collectionDtos': json.dumps(numList),
            'yjhbid': self.ep.getHbList('CNY'),
            'yuanjia': res['data']['dataList'][0]['jiage'],
            'cejia': res['data']['dataList'][0]['jiage'],
            'ydlaiyuan': '订购',
            'ydhbid': self.ep.getHbList('CNY'),
            'jiage': res['data']['dataList'][0]['jiage'],
            'taojia': res['data']['dataList'][0]['jiage'],
            'jzleixing': '纸张',
            'zdfangshi': '平装',
            'juance': 1,
            'fuben': res['data']['dataList'][0]['ceshu'],
            'sshao': r['data']['sshao'],
            'ydRecord': res['data']['dataList'][0]['ydRecord'],
            'ydsmid': res['data']['dataList'][0]['ydsmid'],
            'ydjge': res['data']['dataList'][0]['jiage']
        }).json()
        return result['message']

if __name__ == '__main__':
    print(InterviewPage().subscriptionVerify())