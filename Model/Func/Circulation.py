# -*- coding: utf-8 -*-
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage

class CirculationPage:

    def __init__(self, loginName, loginPwd):
        self.rp = RequestsPage()
        self.ep = ElibPage(loginName, loginPwd)


    def BRRManage(self):
        """
        借还续功能验证
        :return: None
        """
        for r2 in self.getReaderForAdd():
            print(self.operateBook(r2, '借'))
            print(self.operateBook(r2, '续'))
            print(self.operateBook(r2, '还'))

        for r1 in self.getReader():
            print(self.operateBook(r1, '借'))
            print(self.operateBook(r1, '续'))
            print(self.operateBook(r1, '还'))

    def getReader(self):
        readerList = list()
        # for i in self.ep.getDzlxid('more'):
        for data in self.ep.getReaderList()['data']['dataList']:
            # isOverTime = False
            # 判断是否超借
            r = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/curBro', {
                'userToken': self.ep.getUserToken(),
                'readerBarcode': data['dzzhao']
            }).json()
            if len(r['data']) == 0:
                readerList.append(data['dzzhao'])
                break
            # for d in r['data']:
            #     if d['jyztai'] == '超期':
            #         isOverTime = True
            #         break
            # if isOverTime is False:
        return tuple(readerList)

    def getReaderForAdd(self):
        """
        创建读者
        :return: Tuple
        """
        readerList = list()
        for n in self.rp.getRandomReaderID():
            # 发送添加读者的请求
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/readerManager/readerManagerSave', {
                "userToken": self.ep.getUserToken(),
                "dzzhao": n,      # 读者证号
                "xming": n,       # 姓名
                "ztai": "正常",       # 状态
                "mima": "123456",       # 密码
                "dzlxid": self.ep.getDzlxid(isMore=False),       # 读者类型
                "jzrqi": "2020-10-31",      # 截止日期
                "qyrqi": "2020-08-01",      # 启用日期
                "libid": self.ep.getLibid(),        # 馆id
                "smrz": "0",
                "zhuanye": "其他",
                "zhiwu": "无",
                "zcheng": "无",
                "xueli": "其他",
                "xingbie": self.ep.getXingbie(),
                "yajin": "100",
                "zhiye": "其他",
                "jycshu": "0",
                "yycshu": "0",
                "xjcshu": "0",
                "wzcshu": "0",
                "gjhjcshu": "0",
                "qkuan": "0",
                "dzdw": self.rp.randomValue(self.ep.getDzdw())
                # "registerPlaceId": self.rp.randomValue(self.ep.getRegisterPlaceId())       # 办证地点
            }).json()
            if res['message'] == '操作成功!':
                readerList.append(n)
                return tuple(readerList)



    def operateBook(self, reader, state):
        """
        借书、还书、续借功能
        :param reader: 读者
        :param state: 借 / 续 / 还
        :return: String
        """
        res_sm = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/catalog/catalogue/list', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 1000,
            'userType': 1,
            'dateType': 1
        }).json()
        for data in res_sm['data']['dataList']:
            res_gc = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/book/listByCatalogue', {
                'userToken': self.ep.getUserToken(),
                'pageNumber': 1,
                'pageSize': 1000,
                'marctyId': data['marctyid'],
                'isShow': 0
            }).json()
            # 书目馆藏数量不等于0
            if res_gc['data']['count'] != 0:
                for d in res_gc['data']['page']['dataList']:
                    if d['ztai'] == '在馆' and state == '借':
                        broResult = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/bro', {
                            'userToken': self.ep.getUserToken(),
                            'readerBarcode': reader,
                            'bookBarcode': d['tiaoma']
                        }).json()
                        return broResult['message']     # message=借阅成功
                    elif d['ztai'] == '借出' and state == '续':
                        renResult = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/ren', {
                            'userToken': self.ep.getUserToken(),
                            'readerBarcode': reader,
                            'bookBarcode': d['tiaoma']
                        }).json()
                        return renResult['message']  # message=续借成功！
                    elif d['ztai'] == '借出' and state == '还':
                        retResult = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/ret', {
                            'userToken': self.ep.getUserToken(),
                            'isSameCz': 1,
                            'bookBarcode': d['tiaoma']
                        }).json()
                        return retResult['message']  # message=还书成功！
                    else:
                        # print('数据错误')
                        pass




if __name__ == '__main__':
    CirculationPage('TJ', 'Td123456').BRRManage()
