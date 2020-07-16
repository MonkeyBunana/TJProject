# -*- coding: utf-8 -*-”
from Utils.RequestsUtils import RequestsPage
# from Utils.ReadUtils import ReadPage
from Utils.ElibUtils import ElibPage
from Utils.SqlLiteUtils import DBPage
import time

class Reader:

    def __init__(self):
        self.rp = RequestsPage()
        # self.rpp = ReadPage()
        self.ep = ElibPage()
        self.slp = DBPage('book')

        self.token = self.ep.getUserToken()
        self.libid = self.ep.getLibid()

    def addReader(self):
        """
        创建读者
        :return: 无返回
        """
        l = list()
        # 获取随机值，插如 tb_reader 中
        self.slp.addReader(self.ep.getRandomReaderID())
        # requests 模拟接口必要参数
        method = 'POST'
        url = 'http://192.168.1.47:8080/service/api/e/flow/readerManager/readerManagerSave'
        for n in self.ep.getRandomReaderID():
            sex = self.ep.getXingbie()
            dzdw = self.rp.randomValue(self.ep.getDzdw())
            data = {
                "userToken": self.token,
                "dzzhao": n,      # 读者证号
                "xming": n,       # 姓名
                "ztai": "正常",       # 状态
                "mima": "123456",       # 密码
                "dzlxid": self.ep.getDzlxid(),       # 读者类型
                "jzrqi": "2020-07-31",      # 截止日期
                "qyrqi": "2020-07-08",      # 启用日期
                "libid": self.libid,        # 馆id
                "smrz": "0",
                "zhuanye": "其他",
                "zhiwu": "无",
                "zcheng": "无",
                "xueli": "其他",
                "xingbie": sex,
                "yajin": "0",
                "zhiye": "其他",
                "jycshu": "0",
                "yycshu": "0",
                "xjcshu": "0",
                "wzcshu": "0",
                "gjhjcshu": "0",
                "qkuan": "0",
                "dzdw": dzdw,
                "registerPlaceId": self.rp.randomValue(self.ep.getRegisterPlaceId())       # 办证地点
            }
            if sex == 1:
                l.append((n, '男', dzdw, '', '', 0, 0, 0, 0))
            else:
                l.append((n, '女', dzdw, '', '', 0, 0, 0, 0))
            # 发送添加读者的请求
            self.rp.sendRequest(method=method, url=url, data=data)
        # 添加到数据库中
        self.slp.addReader(l)
        self.slp.addTotal([(len(l), 0, 0, 0, self.rp.nowTime())])


    def deleteReader(self):
        """
        删除读者
        :return: 无返回
        """
        l = list()
        # requests 模拟接口必要参数
        method = 'POST'
        url_1 = 'http://192.168.1.47:8080/service/api/e/flow/readerManager/readerManagerList'
        url_2 = 'http://192.168.1.47:8080/service/api/e/flow/readerManager/readerManagerDel'
        data_1 = {'userToken': self.token, 'libid':	self.libid, 'pageNumber': 1, 'pageSize': 50}
        res_1 = self.rp.sendRequest(method=method, url=url_1, data=data_1).json()
        for dataList in res_1['data']['dataList']:
            # 获取所有读者id，添加到列表中
            l.append(dataList['dzid'])
        data_2 = {
            'userToken': self.token,
            'dzid': ','.join(l)
        }
        # 发送请求删除所有读者
        res_2 = self.rp.sendRequest(method=method, url=url_2, data=data_2)
        # 清空数据库
        self.slp.deleteReader()
        self.slp.deleteTotal()
        self.slp.deleteBook()


if __name__ == '__main__':
    Reader().addReader()
    # print(Reader().getUserToken())
    # for n in Reader().getRandomReaderID():
    #     print(n)
    # Reader().deleteReader()
