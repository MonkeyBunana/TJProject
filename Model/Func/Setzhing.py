# -*- coding: utf-8 -*-
# @Time    : 2020/8/4 11:29
from pprint import pprint

from Utils.ElibUtils import ElibPage
from Utils.RequestsUtils import RequestsPage


class SetzhingPage:

    def __init__(self, loginName, loginPwd):
        self.rp = RequestsPage()
        self.ep = ElibPage(loginName, loginPwd)

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
        if 'message' in res:
            if res['message'] == '操作成功':
                print("书商管理书目列表查询成功")
                # pass
            else:
                print(self.ep.getUsercode(), "书商管理书目列表查询出错")
        else:
            print(self.ep.getUsercode(), "书商管理书目列表查询出错", res)

    def BookmanForFoundgysId(self):
        """
        书商管理列表功能验证
        :return: gysId
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysFind', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 15,
            'flag': 1
        }).json()
        if 'message' in res:
            if res['message'] == '操作成功':
                # print(res['data']['dataList'][0])
                return res['data']['dataList'][0]['gysId']
            else:
                print(self.ep.getUsercode(), "获取书商列表第一条数据书商ID出错")
        else:
            print(self.ep.getUsercode(), "获取书商列表第一条数据书商ID出错", res)

    def BookmanForFoundcygname(self):
        """
        书商管理列表功能验证
        :return: cygname
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysFind', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 15,
            'flag': 1
        }).json()
        if 'message' in res:
            if res['message'] == '操作成功':
                return res['data']['dataList'][0]['cygName']
            else:
                print(self.ep.getUsercode(), "获取书商列表第一条数据成员馆出错")
        else:
            print(self.ep.getUsercode(), "获取书商列表第一条数据成员馆出错", res)

    def BookmanForAdd(self):
        """
        新增书商功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysSave', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'gysCode': '12345',
            'gysName': '12345',
            'gysStat': '正常',
            'gysCred': '0'
        }).json()
        if 'message' in res:
            if res['message'] == '操作成功!':
                print("新增书商成功")
            else:
                print(self.ep.getUsercode(), "新增书商出错")
        else:
            print(self.ep.getUsercode(), "新增书商出错", res)

    def BookmanForMod(self, g_data, c_data):
        """
        修改书商功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysSave', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'gysId': g_data,
            'gysCode': 'SSDM-02',
            'gysName': '南方书店',
            'gysStat': '正常',
            'gysCred': 0,
            'cygName': c_data
        }).json()
        if 'message' in res:
            if res['message'] == '操作成功!':
                print("修改书商成功")
            else:
                print(res)
                print(self.ep.getUsercode(), "修改书商出错")
        else:
            print(self.ep.getUsercode(), "修改书商出错", res)



    def BookmanForDel(self, g_data):
        """
        删除书商功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/sys/setup/param/gysDel', {
            'userToken': self.ep.getUserToken(),
            'gysId': g_data
        }).json()
        if 'message' in res:
            if res['message'] == '操作成功!':
                print("删除书商成功")
            else:
                print(res)
                print(self.ep.getUsercode(), "删除书商出错")
        else:
            print(self.ep.getUsercode(), "删除书商出错", res)



if __name__ == '__main__':
    shushang = SetzhingPage('TDJay', 'Td123456')
    shushang.BookmanForQuery()
    shushang.BookmanForAdd()
    gysId_data = shushang.BookmanForFoundgysId()
    dcygname_data = shushang.BookmanForFoundcygname()
    shushang.BookmanForMod(gysId_data, dcygname_data)
    # shushang.BookmanForDel(gysId_data)
