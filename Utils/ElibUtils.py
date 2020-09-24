# -*- coding: utf-8 -*-”
import random
from Utils.RequestsUtils import RequestsPage
from Utils.AESUtils import AesPage
from Utils.ExceptionUtils import ExceptionPage
from sys import _getframe


class ElibPage(object):

    # __instance = None

    # python3 单例模式
    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super(ElibPage, cls).__new__(cls)
    #     return cls.__instance

    def __init__(self, loginName, loginPwd, isAes='yes'):
        self.rp = RequestsPage()
        self.baseUrl = 'http://192.168.1.47:8081'
        # self.baseUrl = 'http://tsgl.geiec.cn'
        self.msg = self.getLoginMsg(loginName, loginPwd, isAes)

    def getUrl(self):
        """
        获取 baseUrl
        :return: String
        """
        return self.baseUrl

    def getUsercode(self):
        """
        获取 管理员用户名
        :return: String
        """
        return self.msg['data']['user']['usercode']

    def getUserToken(self):
        """
        获取 token
        :return: String
        """
        # print(self.msg)
        return self.msg['data']['userToken']

    def getLibid(self):
        """
        获取馆ID
        :return: String
        """
        return self.msg['data']['user']['libId']

    def getLoginMsg(self, loginName, loginPwd, isAes='yes'):
        """
        获取登录用户信息
        :return:
        """
        if isAes == 'yes':
            # yes为密码加密
            loginMsg = self.rp.sendRequest("POST", self.baseUrl + '/service/api/p/login/userLogin', {
                'loginName': loginName,
                'loginPwd': AesPage().AES_encrypt(loginPwd)
            }).json()
        else:
            loginMsg = self.rp.sendRequest("POST", self.baseUrl + '/service/api/p/login/userLogin', {
                'loginName': loginName,
                'loginPwd': loginPwd
            }).json()
        return loginMsg


    def getGysid(self, isMore=True):
        """
        获取供应商ID （暂时先只取第一个供应商）
        :return: String / Tuple
        """
        try:
            gysId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/gysFind', {
            'userToken': self.getUserToken(),
            'flag': 1,
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                gysId['message']
            ).ErrorTemplate(gysId, 'gysId', isMore)
        except Exception as e:
            print(e)

    def getLtlxid(self, isMore=True):
        """
        获取流通类型ID
        :return: String / Tuple
        """
        try:
            ltlxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/flowParameters/flowTypeList', {
            'userToken': self.getUserToken(),
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                ltlxId['message']
            ).ErrorTemplate(ltlxId, 'ltlxid', isMore)
        except Exception as e:
            print(e)

    def getCzid(self, isMore=True):
        """
        获取藏址ID
        :return: String / Tuple
        """
        try:
            czId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/czFind', {
                'userToken': self.getUserToken(),
                'state': -1,
                'pageSize': 1000,
                'pageNumber': 1,
                'libId': self.getLibid()
            }).json()
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                czId['message']
            ).ErrorTemplate(czId, 'czid', isMore)
        except Exception as e:
            print(e)

    def getYslxid(self, isMore=True):
        """ 设置 -> 预算类型
        获取预算类型ID  （暂时先只取第一个预算）
        :return: String / Tuple
        """
        try:
            yslxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/yslxFind', {
                'userToken': self.getUserToken(),
                'flag': 0,
                'pageSize': 1000,
                'pageNumber': 1,
                'libId': self.getLibid()
            }).json()
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                yslxId['message']
            ).ErrorTemplate(yslxId, 'yslxid', isMore)
        except Exception as e:
            print(e)

    def getYsid(self, isMore=True):
        """ 设置 -> 预算管理
        获取预算管理ID
        :return: String / Tuple
        """
        ysId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/ysFind', {
            'userToken': self.getUserToken(),
            'flag': 0,
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
        try:
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                ysId['message']
            ).ErrorTemplate(ysId, 'ysid', isMore)
        except Exception as e:
            print(e)

    def getBatchid(self, isMore=True):
        """
        获取编目批次ID
        :return: Tuple
        """
        batchId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/catalog/other/searchBatch', {
            'userToken': self.getUserToken(),
            'flag': 1,
            'pageSize': 1000,
            'pageNumber': 1,
            'batchStatus': '正常',
            'libId': self.getLibid()
        }).json()
        try:
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                batchId['message']
            ).ErrorTemplate(batchId, 'batchId', isMore)
        except Exception as e:
            print(e)


    def getRegisterPlaceId(self, isMore=True):
        """
        获取办证地点ID
        :return: Tuple / String
        """
        registerPlaceId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/registerPlace/list', {
            'userToken': self.getUserToken(),
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
        try:
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                registerPlaceId['message']
            ).ErrorTemplate(registerPlaceId, 'registerPlaceId', isMore)
        except Exception as e:
            print(e)

    def getDzlxid(self, isMore=True):
        """
        获取读者类型
        :return: Tuple / String
        """
        dzlxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/flowParameters/readerTypeList', {
            'userToken': self.getUserToken(),
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
        try:
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                dzlxId['message']
            ).ErrorTemplate(dzlxId, 'dzlxid', isMore)
        except Exception as e:
            print(e)

    def getFblxid(self, isMore=True):
        """
        获取分编类型
        :return: Tuple / String
        """
        marcFBId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/marcFb', {
            'userToken': self.getUserToken(),
            'libId': self.getLibid()
        }).json()
        marcFBList = list()
        try:
            if marcFBId['code'] == 0:
                # data 存在于 response 中
                if 'data' in marcFBId:
                    for data in marcFBId['data']['list']:
                        marcFBList.append(data['marcfbid'])
                    if isMore is True:
                        return marcFBList
                    else:
                        return marcFBList[0]

            # return ExceptionPage(
            #     _getframe().f_code.co_filename,
            #     _getframe().f_code.co_name,
            #     marcFBId['message']
            # ).ErrorTemplate(marcFBId, 'marcfbid', isMore)
        except Exception as e:
            print(e)

    def getZdpcid(self, isMore=True):
        """
        获取征订目录
        :return: Tuple / String
        """
        zdpcId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/zdpcList', {
            'userToken': self.getUserToken()
        }).json()
        try:
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                zdpcId['message']
            ).ErrorTemplate(zdpcId, 'zdpcid', isMore)
        except Exception as e:
            print(e)

    def getYdd(self, yddDaima='daimaCs', yddIsWork=True):
        """ 采访 -> 预订单管理
        获取预定单
        :param yddDaima: 添加预订单时添加的预订单名称
        :param yddIsWork: 添加预订单时是否设置为工作预订单
        :return: Tuple
        """
        # 查询
        ydd = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/yd/pcSearch', {
            'userToken': self.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'flag': 1
        }).json()
        yddList = list()
        try:
            # code 为 0，返回正确
            if ydd['code'] == 0:
                # data 存在于 response 中
                if 'data' in ydd:
                    # 如果 dataList 为空，则添加并更新数据
                    if len(ydd['data']['dataList']) == 0:
                        self.addYdd(yddDaima, yddIsWork)
                        ydd = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/yd/pcSearch', {
                            'userToken': self.getUserToken(),
                            'pageNumber': 1,
                            'pageSize': 50,
                            'flag': 1
                        }).json()
                    # 循环 dataList, 获取所有 ydpcid, 并返回一个元祖
                    for i in ydd['data']['dataList']:
                        yddList.append(i['ydpcid'])
                    return tuple(yddList)
                else:
                    raise ExceptionPage(
                        _getframe().f_code.co_filename,
                        _getframe().f_code.co_name,
                        'data 字段找不到'
                    )
            else:
                raise ExceptionPage(
                    _getframe().f_code.co_filename,
                    _getframe().f_code.co_name,
                    ydd['message']
                )
        except Exception as e:
            print(e)

    def addYdd(self, daima='daimaCs', isWork=True):
        """ 采访 -> 预订单管理
        新增预订单
        :param daima: 添加预订单时添加的预订单名称
        :param isWork: 添加预订单时是否设置为工作预订单
        :return: <[Response 200]>
        """
        return self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/yd/pcAdd', {
            'userToken': self.getUserToken(),
            'daima': daima,
            'libid': self.getLibid(),
            'gysid': self.getGysid(isMore=False),
            'ysid': self.getYsid(isMore=False),
            'isWork': isWork
        }).json()

    def getYsd(self, ysdDaima='daimaCs', ysdIsWork=True):
        """ 采访 -> 验收单管理
        获取验收单
        :param ysdDaima: 添加预订单时添加的验收单名称
        :param ysdIsWork: 添加预订单时是否设置为工作验收单
        :return: Tuple
        """
        # 查询
        ysd = self.rp.sendRequest('POST', self.baseUrl + '/service/api/e/interview/ys/pcSearch', {
            'userToken': self.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'flag': 1
        }).json()
        ysdList = list()
        try:
            # code 为 0，返回正确
            if ysd['code'] == 0:
                # data 存在于 response 中
                if 'data' in ysd:
                    # 如果 dataList 为空，则添加并更新数据
                    if len(ysd['data']['dataList']) == 0:
                        self.addYsd(ysdDaima, ysdIsWork)
                        ysd = self.rp.sendRequest('POST', self.baseUrl + '/service/api/e/interview/ys/pcSearch', {
                            'userToken': self.getUserToken(),
                            'pageNumber': 1,
                            'pageSize': 50,
                            'flag': 1
                        }).json()
                    # 循环 dataList, 获取所有 yspcid, 并返回一个元祖
                    for i in ysd['data']['dataList']:
                        ysdList.append(i['yspcid'])
                    return tuple(ysdList)
                else:
                    raise ExceptionPage(
                        _getframe().f_code.co_filename,
                        _getframe().f_code.co_name,
                        'data 字段找不到'
                    )
            else:
                raise ExceptionPage(
                    _getframe().f_code.co_filename,
                    _getframe().f_code.co_name,
                    ysd['message']
                )
        except Exception as e:
            print(e)

    def addYsd(self, daima='daimaCs', isWork=True):
        """ 采访 -> 验收单管理
        新增验收单
        :param daima: 添加预订单时添加的验收单名称
        :param isWork: 添加预订单时是否设置为工作验收单
        :return: <[Response 200]>
        """
        return self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/interview/ys/pcSave', {
            'userToken': self.getUserToken(),
            'daima': daima,
            'libid': self.getLibid(),
            'gysid': self.getGysid(isMore='NO'),
            'ysid': self.getYsid(isMore='NO'),
            'isWork': isWork
        }).json()

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


    def getHbList(self, isMore=True):
        """
        货币列表 CNY
        :param isMore: YES输出元祖，NO输出字符串
        :return: String
        """
        hb = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/hbList', {
            'userToken': self.getUserToken(),
            'libId': self.getLibid()
        }).json()
        try:
            return ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                hb['message']
            ).ErrorTemplate(hb, 'hbid', isMore)

        except Exception as e:
            print(e)

    def getReaderList(self, ztai='正常', qkuan=0):
        if qkuan == 0 and qkuan == 1:
            res = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/flow/readerManager/readerManagerList', {
                'userToken': self.getUserToken(),
                'libid': self.getLibid(),
                'pageNumber': 1,
                'pageSize': 50,
                'ztai': ztai,
                'qkuan': qkuan
            }).json()
        else:
            res = self.rp.sendRequest('POST', self.getUrl() + '/service/api/e/flow/readerManager/readerManagerList', {
                'userToken': self.getUserToken(),
                'libid': self.getLibid(),
                'pageNumber': 1,
                'pageSize': 50,
                'ztai': ztai
            }).json()
        return res

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
    print(ElibPage('YZ', 'Td123456').getLibid())
