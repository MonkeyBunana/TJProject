# -*- coding: utf-8 -*-”
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage
from Utils.SqlLiteUtils import DBPage

class Reader:

    def __init__(self):
        self.rp = RequestsPage()
        # self.rpp = ReadPage()
        self.ep = ElibPage('YZ', 'Td123456')
        self.slp = DBPage('book')

    def addReader(self):
        """
        创建读者
        :return: 无返回
        """
        l = list()
        # 获取随机值，插如 tb_reader 中
        # self.slp.addReader(self.ep.getRandomReaderID())
        for n in self.rp.getRandomReaderID():
            sex = self.ep.getXingbie()
            dzdw = self.rp.randomValue(self.ep.getDzdw())
            if sex == 1:
                l.append((n, '男', dzdw, '', '', 0, 0, 0, 0))
            else:
                l.append((n, '女', dzdw, '', '', 0, 0, 0, 0))
            # 发送添加读者的请求
            self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/readerManager/readerManagerSave', {
                "userToken": self.ep.getUserToken(),
                "dzzhao": n,      # 读者证号
                "xming": n,       # 姓名
                "ztai": "正常",       # 状态
                "mima": "123456",       # 密码
                "dzlxid": self.ep.getDzlxid(isMore=False),       # 读者类型
                "jzrqi": self.rp.nowTime(ty='end'),      # 截止日期
                "qyrqi": self.rp.nowTime(ty='now'),      # 启用日期
                "libid": self.ep.getLibid(),        # 馆id
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
            })
        # 添加到数据库中
        self.slp.addReader(l)
        self.slp.addTotal([(len(l), 0, 0, 0, str(self.rp.nowTime()))])


    def deleteReader(self):
        """
        删除读者
        :return: 无返回
        """
        l = list()
        # requests 模拟接口必要参数
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/readerManager/readerManagerList', {
            'userToken': self.ep.getUserToken(),
            'libid':	self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        for dataList in res['data']['dataList']:
            # 获取所有读者id，添加到列表中
            l.append(dataList['dzid'])
        # 发送请求删除所有读者
        self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/readerManager/readerManagerDel', {
            'userToken': self.ep.getUserToken(),
            'dzid': ','.join(l)
        })
        # 清空数据库
        self.slp.deleteReader()


if __name__ == '__main__':
    Reader().addReader()
    # print(Reader().getUserToken())
    # for n in Reader().getRandomReaderID():
    #     print(n)
    # Reader().deleteReader()
