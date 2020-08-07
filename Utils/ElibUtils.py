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

    def getYslxid(self):
        """ 设置 -> 预算类型
        获取预算类型ID  （暂时先只取第一个预算）
        :return: String
        """
        yslxId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/yslxFind', {
            'userToken': self.getUserToken(),
            'flag': 0,
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
        # code 为 0，返回正确
        if yslxId['code'] == 0:
            # data 存在于 response 中
            if 'data' in yslxId:
                if len(yslxId['data']['dataList']) == 0:
                    return '设置 -> 预算类型 -> 查询：缺少默认值'
                return yslxId['data']['dataList'][0]['yslxid']
            else:
                return '设置 -> 预算类型 -> 查询：data not found'
        else:
            return '采访 -> 预算类型 -> 查询：%s' % yslxId

    def getYsid(self):
        """ 设置 -> 预算管理
        获取预算管理ID
        :return: String
        """
        ysId = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/sys/setup/param/ysFind', {
            'userToken': self.getUserToken(),
            'flag': 0,
            'pageSize': 1000,
            'pageNumber': 1,
            'libId': self.getLibid()
        }).json()
        # code 为 0，返回正确
        if ysId['code'] == 0:
            # data 存在于 response 中
            if 'data' in ysId:
                if len(ysId['data']['dataList']) == 0:
                    return '设置 -> 预算管理 -> 查询：缺少默认值'
                return ysId['data']['dataList'][0]['ysid']
            else:
                return '设置 -> 预算管理 -> 查询：data not found'
        else:
            return '采访 -> 预算管理 -> 查询：%s' % ysId

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
                return '采访 -> 预订单管理 -> 查询：data not found'
        else:
            return '采访 -> 预订单管理 -> 查询：%s' % ydd

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
                'gysid': self.getGysid(),
                'ysid': self.getYsid(),
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
                return '采访 -> 验收单管理 -> 查询：data not found'
        else:
            return '采访 -> 验收单管理 -> 查询：%s' % ysd

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
            'gysid': self.getGysid(),
            'ysid': self.getYsid(),
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

    def getHbList(self, hbcode='CNY'):
        """
        货币列表 CNY
        :param hbcode: 输入你要的货币code，输出相应货币id
        :return: String
        """
        hb = self.rp.sendRequest("POST", self.baseUrl + '/service/api/e/parameter/hbList', {
            'userToken': self.getUserToken(),
            'libId': self.getLibid()
        }).json()
        # code 为 0，返回正确
        if hb['code'] == 0:
            # data 存在于 response 中
            if 'data' in hb:
                # 如果 dataList 为空，则添加并更新数据
                if len(hb['data']) == 0:
                    return '设置 -> 货币汇率 -> 查询：缺少默认值'
                for i in hb['data']:
                    if i['hbcode'] == hbcode:
                        return i['hbid']
                    else:
                        return '设置 -> 货币汇率 -> 查询：找不到 %s 这个hbcode'
            else:
                return '设置 -> 货币汇率 -> 查询：data not found'
        else:
            return '设置 -> 货币汇率 -> 查询：%s' % hb

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
    print(ElibPage('zhonglilong', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D').getDzlxid('more'))
