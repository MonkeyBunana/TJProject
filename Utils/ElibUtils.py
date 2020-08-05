# -*- coding: utf-8 -*-”
import random
from Utils.RequestsUtils import RequestsPage
from Utils.AESUtils import AesPage

class ElibPage:

    def __init__(self, loginName, loginPwd, isAes='yes'):
        self.rp = RequestsPage()

        self.baseUrl = 'http://192.168.1.120:8080'
        if isAes == 'yes':
            self.loginMsg = self.rp.sendRequest("POST", self.baseUrl + '/service/api/p/login/userLogin', {
                'loginName': loginName,
                'loginPwd': AesPage().AES_encrypt(loginPwd)
            }).json()
        else:
            self.loginMsg = self.rp.sendRequest("POST", self.baseUrl + '/service/api/p/login/userLogin', {
                'loginName': loginName,
                'loginPwd': loginPwd
            }).json()

        if self.getLoginMsg()['code'] == 0:
            self.gysId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/gysFind', {
                'userToken': self.getUserToken(),
                'flag': 1,
                'pageSize': 1000,
                'pageNumber': 1,
                'libId': self.getLibid()
            }).json()
            self.ltlxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/flowParameters/flowTypeList', {
                'userToken': self.getUserToken(),
                'pageSize': 1000,
                'pageNumber': 1,
                'libId': self.getLibid()
            }).json()
            self.czId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/czFind', {
                'userToken': self.getUserToken(),
                'state': -1,
                'pageSize': 1000,
                'pageNumber': 1,
                'libId': self.getLibid()
            }).json()
            self.yslxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/yslxFind', {
                'userToken': self.getUserToken(),
                'flag': 0,
                'pageSize': 1000,
                'pageNumber': 1,
                'libId': self.getLibid()
            }).json()
            self.batchId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/catalog/other/searchBatch', {
                'userToken': self.getUserToken(),
                'flag': 1,
                'pageSize': 1000,
                'pageNumber': 1,
                'batchStatus': '正常',
                'libId': self.getLibid()
            }).json()
            self.registerPlaceId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/registerPlace/list', {
                                                           'userToken': self.getUserToken(),
                                                           'pageSize': 1000,
                                                           'pageNumber': 1,
                                                           'libId': self.getLibid()
                                                       }).json()
            self.dzlxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/flowParameters/readerTypeList', {
                                                  'userToken': self.getUserToken(),
                                                  'pageSize': 1000,
                                                  'pageNumber': 1,
                                                  'libId': self.getLibid()
                                              }).json()
            self.marcFBId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/marcFb', {
                'userToken': self.getUserToken(),
                'libId': self.getLibid()
            }).json()
            self.zdpcId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/zdpcList', {
                'userToken': self.getUserToken()
            }).json()
            self.ydd = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/yd/pcSearch', {
                'userToken': self.getUserToken(),
                'pageNumber': 1,
                'pageSize': 50,
                'flag': 1
            }).json()
            self.ysd = self.rp.sendRequest('POST', self.baseUrl + '/service/api/e/interview/ys/pcSearch', {
                'userToken': self.getUserToken(),
                'pageNumber': 1,
                'pageSize': 50,
                'flag': 1
            }).json()
            self.hb = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/hbList', {
                'userToken': self.getUserToken(),
                'libId': self.getLibid()
            }).json()


    def getUrl(self):
        """
        获取 baseUrl
        :return: String
        """
        return self.baseUrl

    def getUsercode(self):
        """
        获取 baseUrl
        :return: String
        """
        return self.loginMsg['data']['user']['usercode']

    def getUserToken(self):
        """
        获取 token
        :return: String
        """
        return self.loginMsg['data']['userToken']

    def getLibid(self):
        """
        获取馆ID
        :return: String
        """
        return self.loginMsg['data']['user']['libId']

    def getLoginMsg(self):
        """
        获取登录用户信息
        :return:
        """
        return self.loginMsg

    def getGysid(self):
        """
        获取供应商ID （暂时先只取第一个供应商）
        :return: String
        """
        return self.gysId['data']['dataList'][0]['gysId']

    def getLtlxid(self):
        """
        获取流通类型ID （暂时先只取第一个流通类型）
        :return: String
        """
        return self.ltlxId['data']['dataList'][0]['ltlxid']

    def getCzid(self):
        """
        获取藏址ID
        :return: Tuple
        """
        czList = list()
        for cz in self.czId['data']['dataList']:
            czList.append(cz['czid'])
        return tuple(czList)

    def getYsuanid(self):
        """
        获取预算ID  （暂时先只取第一个预算）
        :return: String
        """
        return self.yslxId['data']['dataList'][0]['yslxid']

    def getBatchid(self):
        """
        获取编目批次ID
        :return: Tuple
        """
        batchList = list()
        for batch in self.batchId['data']['dataList']:
            batchList.append(batch['batchId'])
        return tuple(batchList)

    def getRegisterPlaceId(self):
        """
        获取办证地点ID
        :return: Tuple
        """
        registerPlaceList = list()
        for registerPlace in self.registerPlaceId['data']['dataList']:
            registerPlaceList.append(registerPlace['registerPlaceId'])
        return tuple(registerPlaceList)

    def getDzlxid(self, ty=None):
        """
        获取读者类型
        :return: Tuple / String
        """
        dzlxList = list()
        if ty == 'more':
            for i in self.dzlxId['data']['dataList']:
                    dzlxList.append(i['dzlxid'])
            return tuple(dzlxList)
        else:
            return self.dzlxId['data']['dataList'][0]['dzlxid']

    def getFblxid(self):
        """
        获取分编类型
        :return: String
        """
        return self.marcFBId['data']['list'][0]['marcfbid']

    def getZdpcid(self):
        """
        获取征订目录
        :return: Tuple
        """
        zdpcList = list()
        for i in self.zdpcId['data']:
            zdpcList.append(i['zdpcid'])
        return tuple(zdpcList)

    def getYdd(self):
        """
        获取预定单
        :return: Tuple
        """
        yddList = list()
        for i in self.ydd['data']['dataList']:
            yddList.append(i['ydpcid'])
        return tuple(yddList)

    def getYsd(self):
        """
        获取验收单
        :return: Tuple
        """
        ysdList = list()
        for i in self.ysd['data']['dataList']:
            ysdList.append(i['yspcid'])
        return tuple(ysdList)

    def getZdsmReserve(self, marcid=None, zdpcid=None, zdsmid=None):
        """
        征订书目-跳转预订
        参数传递： 征订批次->预订（zdpcid,zdsmid）。直接预订（marcid）
        :param zdsmid:  征订书目id
        :param zdpcid:  征订批次id
        :param marcid:  marcid
        :return: req(<Response [200]>)
        """
        if zdpcid is None and zdsmid is None and marcid is not None:
            return self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/zdsm/reserve', {
            'userToken': self.getUserToken(),
            'marcid': marcid
        }).json()
        if zdpcid is not None and zdsmid is not None and marcid is None:
            return self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/zdsm/reserve', {
                'userToken': self.getUserToken(),
                'zdpcid': zdpcid,
                'zdsmid': zdsmid
            }).json()

    def getHbList(self, hbcode):
        """
        货币列表 CNY
        :return: String
        """
        for i in self.hb['data']:
            if i['hbcode'] == hbcode:
                return i['hbid']

    def getXingbie(self):
        """
        获取性别
        :return: Int
        """
        return random.randint(0, 1)

    def getDzdw(self):
        """
        获取工作单位
        :return: Tuple
        """
        dzdw = ("asd1", "asd2", "asd3")
        return dzdw



if __name__ == '__main__':
    print(ElibPage('zhonglilong', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D').getDzlxid('more'))
