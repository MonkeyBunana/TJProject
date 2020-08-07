# -*- coding: utf-8 -*-
import random
import json
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage
from urllib import parse

class InterviewPage(ElibPage):

    def __init__(self, loginName, loginPwd):
        super().__init__(loginName, loginPwd)
        self.rp = RequestsPage()

    def ZDManage(self):
        # print(self.subscriptionBooksImport())
        print(self.subscriptionBooks())
        print(self.directSubscription())
        print(self.subscriptionVerify())
        print(self.directVerify())


    def subscriptionBooksImport(self):
        """
        征订书目导入功能
        :return:
        """
        with open('D:\Cache\Project\TJProject\list.xls', mode="rb+") as f:  # 打开文件
            file = {
                "excel": ('list.xls', f.read()),  # 引号的file是接口的字段，后面的是文件的名称、文件的内容
                "userToken": self.getUserToken(),  # 如果接口中有其他字段也可以加上
            }
        res = self.rp.sendRequest('FILE', self.getUrl() + '/service/api/e/interview/file/zdsmI', file).json()
        r = self.rp.sendRequest('FILE', self.getUrl() + '/service/api/e/interview/zdsm/import/main', {
            'userToken': self.getUserToken(),
            'path': res['data']['path'],
            'marcfbid': self.getFblxid(),
            'zdpcid': self.getZdpcid()[0],
            'isbn': 'ISBN,0',
            'ztming': '正题名,0'
        }).json()
        return r['message']

    def subscriptionBooks(self):
        """
        征订书目预订功能
        :return:
        """
        # 先在 预订单管理 设置第一个为工作预定单
        self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.getUserToken(),
            'ydpcid': self.getYdd()[0]
        })
        # 获取征订目录列表
        res = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/zdpc/search', {
            'userToken': self.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        # 获取图书信息
        r = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/zdsm/search', {
            'userToken': self.getUserToken(),
            'zdpcid': res['data']['dataList'][0]['zdpcid'],
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        # 判断图书信息中价格是否存在
        price = 0
        if 'jge' in dict(r):
            price = int(self.rp.matchNumber(r['data']['page']['dataList'][0]['jge']))
        # 获取预订单信息
        yd = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/pcList', {
            'userToken': self.getUserToken()
        }).json()
        # 预订
        result = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/smSave', {
            'userToken': self.getUserToken(),
            'cygName': yd['data'][0]['cygName'],
            'ysName': yd['data'][0]['ysName'],
            'marcid': r['data']['page']['dataList'][0]['marcid'],
            'gysName': yd['data'][0]['gysName'],
            'ydbhao': '',
            'ydpcid': yd['data'][0]['ydpcid'],
            'ceshu': 1,
            'ydlaiyuan': '订购',
            'yjhbid': self.getHbList('CNY'),
            'jzleixing': '纸张',
            'yuanjia': price,
            'zdfangshi': '平装',
            'ydhbid': self.getHbList('CNY'),
            'juance': 1,
            'jiage': price,
            'fuzhu': '',
            'zdpcdm': res['data']['dataList'][0]['zdpcdm'],
            'ydpcdm': self.getZdsmReserve(zdpcid=res['data']['dataList'][0]['zdpcid'], zdsmid=r['data']['page']['dataList'][0]['zdsmid']),
            'ysCode': yd['data'][0]['ysCode'],
            'zdpcid': self.getZdpcid()[0],
            'gysCode': yd['data'][0]['gysCode'],
            'ydleixing': '征订预订'
        }).json()
        print(result['message'])  # 操作成功!

    def directSubscription(self):
        """
        直接预订功能
        :return:
        """
        # 先在 预订单管理 设置第一个为工作预定单
        self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.getUserToken(),
            'ydpcid': self.getYdd()[0]
        })
        # 获取图书信息
        res = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/searchBook', {
            'userToken': self.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'flag': 1
        }).json()
        # 征订书目-直接预订
        r = self.getZdsmReserve(marcid=res['data']['dataList'][0]['marcid'])
        # 预定
        result = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/smSave', {
            'userToken': self.getUserToken(),
            'cygName': r['data']['cygName'],
            'ysName': r['data']['ysName'],
            'marcid': r['data']['marcid'],
            'gysName': r['data']['gysName'],
            'ydbhao': '',
            'ydpcid': r['data']['ydpcid'],
            'ceshu': 1,
            'ydlaiyuan': '订购',
            'yjhbid': self.getHbList('CNY'),
            'jzleixing': '纸张',
            'yuanjia': 0,
            'zdfangshi': '平装',
            'ydhbid': self.getHbList('CNY'),
            'juance': 1,
            'jiage': 0,
            'fuzhu': '',
            'ydpcdm': 1,
            'ysCode': r['data']['ysCode'],
            'gysCode': r['data']['gysCode'],
            'ydleixing': '直接预订'
        }).json()
        print(result['message'])  # 操作成功!  已超出预算金额，不能预订！

    def subscriptionVerify(self):
        """
        预订验收功能
        :return:
        """
        # 先在 验收单管理 设置第一个为工作验收单
        self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.getUserToken(),
            'yspcid': self.getYsd()[0]
        })
        # 获取图书信息
        res = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/smSearch', {
            'userToken': self.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'from': 1,
            'flag': 1
        }).json()
        # 获取索书号
        r = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/ys/curSshao', {
            'userToken': self.getUserToken(),
            'marcid': res['data']['dataList'][0]['marcid']
        }).json()
        # 验收
        numList = list()
        for i in range(res['data']['dataList'][0]['ceshu']):
            numDict = dict()
            numDict['barcode'] = "TS" + str(random.randint(1, 10000)).zfill(5)
            numDict['libId'] = self.getLibid()
            numDict['czId'] = self.getCzid()[0]
            numDict['ltlxId'] = self.getLtlxid()
            numList.append(numDict)
        # '['
        #     '{"barcode": "test100", "libId": "2", "czId": "ebd840b69bc04948859cd05a4da638b3", "ltlxId": "1"},'
        #     '{"barcode": "test101", "libId": "2", "czId": "ebd840b69bc04948859cd05a4da638b3", "ltlxId": "1"}'
        # ']',

        result = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/ys/smSave', {
            'userToken': self.getUserToken(),
            'marcid': res['data']['dataList'][0]['marcid'],
            'yslxing': '预订验收',
            'yspcid': self.getYsd()[0],
            'collectionDtos': json.dumps(numList),
            'yjhbid': self.getHbList('CNY'),
            'yuanjia': res['data']['dataList'][0]['jiage'],
            'cejia': res['data']['dataList'][0]['jiage'],
            'ydlaiyuan': '订购',
            'ydhbid': self.getHbList('CNY'),
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
        print(result['message'])

    def directVerify(self):
        """
        快捷验收功能
        :return:
        """
        # 先在 验收单管理 设置第一个为工作验收单
        self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/work/save', {
            'userToken': self.getUserToken(),
            'yspcid': self.getYsd()[0]
        })
        # 获取图书信息
        res = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/searchBook', {
            'userToken': self.getUserToken(),
            'pageNumber': 16019,
            'pageSize': 50,
            'flag': 1
        }).json()
        # 获取索书号
        r = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/yd/searchBookByMarcid', {
            'userToken': self.getUserToken(),
            'marcid': res['data']['dataList'][0]['marcid']
        }).json()
        print(r['data']['sshao'])
        # 验收
        numList = list()
        for i in range(res['data']['dataList'][0]['fuben']+1):
            numDict = dict()
            numDict['barcode'] = "TS" + str(random.randint(1, 10000)).zfill(5)
            numDict['libId'] = self.getLibid()
            numDict['czId'] = self.getCzid()[0]
            numDict['ltlxId'] = self.getLtlxid()
            numList.append(numDict)

        result = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/interview/ys/smSave', {
            'userToken': self.getUserToken(),
            'marcid': res['data']['dataList'][0]['marcid'],
            'yslxing': '直接验收',
            'yspcid': self.getYsd()[0],
            'collectionDtos': json.dumps(numList),
            'yjhbid': self.getHbList('CNY'),
            'yuanjia': r['data']['jge'],
            'cejia': r['data']['jge'],
            'ydlaiyuan': '订购',
            'ydhbid': self.getHbList('CNY'),
            'jiage': r['data']['jge'],
            'taojia': r['data']['jge'],
            'jzleixing': '纸张',
            'zdfangshi': '平装',
            'juance': 1,
            'fuben': res['data']['dataList'][0]['fuben']+1,
            'sshao': r['data']['sshao'],
        }).json()
        print(result['message'])


if __name__ == '__main__':
    print(InterviewPage('cwq', '84548081').subscriptionBooksImport())