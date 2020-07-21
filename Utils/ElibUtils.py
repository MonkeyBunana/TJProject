# -*- coding: utf-8 -*-”
import json
import random
from Utils.RequestsUtils import RequestsPage
from Utils.ReadUtils import ReadPage
from Utils.SqlLiteUtils import DBPage

class ElibPage:

    def __init__(self):
        self.rp = RequestsPage()
        # self.rpp = ReadPage()
        self.slp = DBPage('book')


    def getUserToken(self):
        """
        获取 token
        :return: String
        """
        method = 'POST'
        url = 'http://192.168.1.47:8080/service/api/p/login/userLogin'
        data = {"loginName": "TJ", "loginPwd": "6Tet8CNiT2soE8BiYcXR%2FA%3D%3D"}
        res = self.rp.sendRequest(method=method, url=url, data=data)
        return dict(json.loads(res.text))['data']['userToken']

    def getRandomReaderID(self):
        """
        获取随机用户名
        :return: List
        """
        name = set()
        while len(name) < 20:
            num = random.randint(1, 10000)
            name.add("DZ" + str(num).zfill(5))
        return list(name)

    def getLibid(self):
        """
        获取馆ID
        :return: String
        """
        return 'a4854ce9259f465ab6f32ad296698eff'

    def getGysid(self):
        """
        获取供应商ID
        :return: String
        """
        return 'e3939d11e03b4471bd5662cb2798c11e'

    def getLtlxid(self):
        """
        获取流通类型ID
        :return: String
        """
        return 'bca922ec5d204407a35730e8b9800004'

    def getCzid(self):
        """
        获取藏址ID
        :return: Tuple
        """
        czid = ('05e4efc8f0b44bb9b7030fb4fafd1495', '1bf1f8b6fd0645bd855d8532d9fe3fc1')
        return czid

    def getYsuanid(self):
        """
        获取预算ID
        :return: String
        """
        return '8f840e57daeb4f9c8b5ab2f1288e5800'

    def getBatchid(self):
        """
        获取编目批次ID
        :return: Tuple
        """
        batchid = ('e04407f77e08484d895c550df3443b08', 'd2a406800e8747b192dcdc1a802ef3f3')
        return batchid

    def getRegisterPlaceId(self):
        """
        获取办证地点ID
        :return: Tuple
        """
        registerPlaceId = ("bb932be5cc0a4a2e980d06dfc6443e36", "4c5c556472d3438fb4ba6d7800d59de1")
        return registerPlaceId

    def getDzlxid(self):
        """
        获取读者类型
        :return: String
        """
        return 'c6f1bc225ca8433ab0dc07d1981532b1'

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
    ElibPage().getUserToken()