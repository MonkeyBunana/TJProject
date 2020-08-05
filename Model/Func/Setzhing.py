# -*- coding: utf-8 -*-
# @Time    : 2020/8/4 11:29
from pprint import pprint

from Utils.ElibUtils import ElibPage
from Utils.RequestsUtils import RequestsPage


class SetzhingPage:

    def __init__(self):
        self.rp = RequestsPage()
        self.ep = ElibPage('hoxx', '123456')

    def BookmanForQuery(self):
        """
        书商管理列表功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysFind', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 15,
            'flag': 1
        }).json()
        if res['message'] == '操作成功':
            print("书商管理书目列表查询成功")
            # pass
        else:
            print("书商管理书目列表查询出错")

    def BookmanForAdd(self):
        """
        新增书商功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysSave', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'gysCode': 'SSDM-01',
            'gysName': '南方书店',
            'gysStat': '正常',
            'gysCred': 0
        }).json()
        if res['message'] == '操作成功':
            print("新增书商成功")
            # pass
        else:
            print(res)
            print(self.ep.getUsercode(), "新增书商失败")

    def BookmanForMod(self):
        """
        修改书商功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysSave', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'gysCode': 'SSDM-01',
            'gysName': '南方书店',
            'gysStat': '正常',
            'gysCred': 0
        }).json()
        if res['message'] == '操作成功!':
            print("修改书商成功")
            # pass
        else:
            print(self.ep.getUsercode(), "修改书商失败")



if __name__ == '__main__':
    # SetzhingPage().BookmanForQuery()
    SetzhingPage().BookmanForAdd()
