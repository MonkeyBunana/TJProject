# -*- coding: utf-8 -*-
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage
import json

class CataloguedPage:


    def __init__(self, loginName, loginPwd):
        self.rp = RequestsPage()
        self.ep = ElibPage(loginName, loginPwd)

    def CataloguedForQuery(self):
        """
        编目管理书目列表功能验证
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/catalog/catalogue/list', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 15,
            'userType': 1,
            'dateType': 1
        }).json()
        print(res)
        if 'message' in res:
            if res['message'] == '操作成功':
                print("编目管理书目列表查询成功")
                # pass
            else:
                print("编目管理书目列表查询出错")
        else:
            print("编目管理书目列表查询出错", res)

    def CataloguedForAdd(self):
        """
        新增编目功能验证
        :return: marctyid  书目编号，定位要编目的书目记录
        """
        data = {"userToken": self.ep.getUserToken(),
                "marcfbid": self.ep.getFblxid(isMore=False),
                "simpleList": [
                    {"fieldName": "分类号", "marcField": "690a", "content": "EC-7", "isEmpty": 1, "sort": 1},
                    {"fieldName": "并列正题名", "marcField": "510a", "content": "", "isEmpty": 1, "sort": 2},
                    {"fieldName": "正题名拼音", "marcField": "2009", "content": "", "isEmpty": 1, "sort": 3},
                    {"fieldName": "国内订购号", "marcField": "092b", "content": "", "isEmpty": 1, "sort": 4},
                    {"fieldName": "语种", "marcField": "101a", "content": "", "isEmpty": 1, "sort": 5},
                    {"fieldName": "期刊价格", "marcField": "011d", "content": "", "isEmpty": 1, "sort": 6},
                    {"fieldName": "ISBN", "marcField": "010a", "content": "508", "isEmpty": 0, "sort": 7},
                    {"fieldName": "责任者拼音", "marcField": "7019", "content": "", "isEmpty": 1, "sort": 8},
                    {"fieldName": "副题名", "marcField": "200e", "content": "", "isEmpty": 1, "sort": 9},
                    {"fieldName": "价格", "marcField": "010d", "content": "", "isEmpty": 1, "sort": 10},
                    {"fieldName": "版次", "marcField": "205a", "content": "", "isEmpty": 1, "sort": 11},
                    {"fieldName": "正题名", "marcField": "200a", "content": "这是正题名", "isEmpty": 0, "sort": 12},
                    {"fieldName": "出版地", "marcField": "210a", "content": "", "isEmpty": 1, "sort": 13},
                    {"fieldName": "其他责任者", "marcField": "200g", "content": "", "isEmpty": 1, "sort": 14},
                    {"fieldName": "页码", "marcField": "215a", "content": "", "isEmpty": 1, "sort": 15},
                    {"fieldName": "统一书刊号", "marcField": "091a", "content": "", "isEmpty": 1, "sort": 16},
                    {"fieldName": "分辑名", "marcField": "200i", "content": "", "isEmpty": 1, "sort": 17},
                    {"fieldName": "版本与书目史附注", "marcField": "305a", "content": "", "isEmpty": 1, "sort": 18},
                    {"fieldName": "内容附注", "marcField": "327a", "content": "", "isEmpty": 1, "sort": 19},
                    {"fieldName": "一般性附注", "marcField": "300a", "content": "", "isEmpty": 1, "sort": 20},
                    {"fieldName": "丛编题名", "marcField": "225a", "content": "", "isEmpty": 1, "sort": 21},
                    {"fieldName": "国外订购号", "marcField": "092c", "content": "", "isEmpty": 1, "sort": 22},
                    {"fieldName": "摘要", "marcField": "330a", "content": "", "isEmpty": 1, "sort": 23},
                    {"fieldName": "尺寸", "marcField": "215e", "content": "", "isEmpty": 1, "sort": 24},
                    {"fieldName": "责任者", "marcField": "200f", "content": "", "isEmpty": 1, "sort": 25},
                    {"fieldName": "相关题名附注", "marcField": "312a", "content": "", "isEmpty": 1, "sort": 26},
                    {"fieldName": "出版社", "marcField": "210c", "content": "", "isEmpty": 1, "sort": 27},
                    {"fieldName": "附件", "marcField": "215b", "content": "", "isEmpty": 1, "sort": 28},
                    {"fieldName": "分辑号", "marcField": "200h", "content": "", "isEmpty": 1, "sort": 29},
                    {"fieldName": "文献类型", "marcField": "200b", "content": "", "isEmpty": 1, "sort": 30},
                    {"fieldName": "丛编责任者", "marcField": "225f", "content": "", "isEmpty": 1, "sort": 31},
                    {"fieldName": "书目控制号", "marcField": "001", "content": "012020", "isEmpty": 1, "sort": 32},
                    {"fieldName": "出版日期", "marcField": "210d", "content": "", "isEmpty": 1, "sort": 33},
                    {"fieldName": "ISRC", "marcField": "016a", "content": "", "isEmpty": 1, "sort": 34},
                    {"fieldName": "主题词", "marcField": "606a", "content": "", "isEmpty": 1, "sort": 35},
                    {"fieldName": "ISSN", "marcField": "011a", "content": "", "isEmpty": 1, "sort": 36},
                    {"fieldName": "出版周期", "marcField": "326a", "content": "", "isEmpty": 1, "sort": 37},
                    {"fieldName": "封面题名", "marcField": "512a", "content": "", "isEmpty": 1, "sort": 38},
                    {"fieldName": "并列题名", "marcField": "200d", "content": "", "isEmpty": 1, "sort": 39}]
                }
        res = self.rp.sendRequest('JSON', self.ep.getUrl() + '/service/api/e/catalog/catalogue/simple/save',
                                  json.dumps(data)).json()
        if 'message' in res:
            if res['message'] == '操作成功!':
                print("新增编目成功")
                return res['data']['marctyid']
            else:
                print("新增编目出错")
        else:
            print("新增编目出错", res)

    def CataloguedForMod(self, cata):
        """
        修改编目功能验证
        marctyid:书目编号，定位要编目的书目记录
        :return: None
        """
        data = {"userToken": self.ep.getUserToken(),
                "marcfbid": self.ep.getFblxid(isMore=False),
                "marctyid": cata,
                "simpleList": [
                    {"fieldName": "分类号", "marcField": "690a", "content": "EC-7", "isEmpty": 1, "sort": 1},
                    {"fieldName": "并列正题名", "marcField": "510a", "content": "", "isEmpty": 1, "sort": 2},
                    {"fieldName": "正题名拼音", "marcField": "2009", "content": "", "isEmpty": 1, "sort": 3},
                    {"fieldName": "国内订购号", "marcField": "092b", "content": "", "isEmpty": 1, "sort": 4},
                    {"fieldName": "语种", "marcField": "101a", "content": "", "isEmpty": 1, "sort": 5},
                    {"fieldName": "期刊价格", "marcField": "011d", "content": "", "isEmpty": 1, "sort": 6},
                    {"fieldName": "ISBN", "marcField": "010a", "content": "5021", "isEmpty": 0, "sort": 7},
                    {"fieldName": "责任者拼音", "marcField": "7019", "content": "", "isEmpty": 1, "sort": 8},
                    {"fieldName": "副题名", "marcField": "200e", "content": "", "isEmpty": 1, "sort": 9},
                    {"fieldName": "价格", "marcField": "010d", "content": "", "isEmpty": 1, "sort": 10},
                    {"fieldName": "版次", "marcField": "205a", "content": "", "isEmpty": 1, "sort": 11},
                    {"fieldName": "正题名", "marcField": "200a", "content": "5021", "isEmpty": 0, "sort": 12},
                    {"fieldName": "出版地", "marcField": "210a", "content": "", "isEmpty": 1, "sort": 13},
                    {"fieldName": "其他责任者", "marcField": "200g", "content": "", "isEmpty": 1, "sort": 14},
                    {"fieldName": "页码", "marcField": "215a", "content": "", "isEmpty": 1, "sort": 15},
                    {"fieldName": "统一书刊号", "marcField": "091a", "content": "", "isEmpty": 1, "sort": 16},
                    {"fieldName": "分辑名", "marcField": "200i", "content": "", "isEmpty": 1, "sort": 17},
                    {"fieldName": "版本与书目史附注", "marcField": "305a", "content": "", "isEmpty": 1, "sort": 18},
                    {"fieldName": "内容附注", "marcField": "327a", "content": "", "isEmpty": 1, "sort": 19},
                    {"fieldName": "一般性附注", "marcField": "300a", "content": "", "isEmpty": 1, "sort": 20},
                    {"fieldName": "丛编题名", "marcField": "225a", "content": "", "isEmpty": 1, "sort": 21},
                    {"fieldName": "国外订购号", "marcField": "092c", "content": "", "isEmpty": 1, "sort": 22},
                    {"fieldName": "摘要", "marcField": "330a", "content": "", "isEmpty": 1, "sort": 23},
                    {"fieldName": "尺寸", "marcField": "215e", "content": "", "isEmpty": 1, "sort": 24},
                    {"fieldName": "责任者", "marcField": "200f", "content": "", "isEmpty": 1, "sort": 25},
                    {"fieldName": "相关题名附注", "marcField": "312a", "content": "", "isEmpty": 1, "sort": 26},
                    {"fieldName": "出版社", "marcField": "210c", "content": "", "isEmpty": 1, "sort": 27},
                    {"fieldName": "附件", "marcField": "215b", "content": "", "isEmpty": 1, "sort": 28},
                    {"fieldName": "分辑号", "marcField": "200h", "content": "", "isEmpty": 1, "sort": 29},
                    {"fieldName": "文献类型", "marcField": "200b", "content": "", "isEmpty": 1, "sort": 30},
                    {"fieldName": "丛编责任者", "marcField": "225f", "content": "", "isEmpty": 1, "sort": 31},
                    {"fieldName": "书目控制号", "marcField": "001", "content": "012020", "isEmpty": 1, "sort": 32},
                    {"fieldName": "出版日期", "marcField": "210d", "content": "", "isEmpty": 1, "sort": 33},
                    {"fieldName": "ISRC", "marcField": "016a", "content": "", "isEmpty": 1, "sort": 34},
                    {"fieldName": "主题词", "marcField": "606a", "content": "", "isEmpty": 1, "sort": 35},
                    {"fieldName": "ISSN", "marcField": "011a", "content": "", "isEmpty": 1, "sort": 36},
                    {"fieldName": "出版周期", "marcField": "326a", "content": "", "isEmpty": 1, "sort": 37},
                    {"fieldName": "封面题名", "marcField": "512a", "content": "", "isEmpty": 1, "sort": 38},
                    {"fieldName": "并列题名", "marcField": "200d", "content": "", "isEmpty": 1, "sort": 39}]
                }
        res = self.rp.sendRequest('JSON', self.ep.getUrl() + '/service/api/e/catalog/catalogue/simple/save',
                                  json.dumps(data)).json()
        if 'message' in res:
            if res['message'] == '操作成功!':
                print("修改编目成功")
            else:
                print("修改编目出错")
        else:
            print("修改编目出错", res)

    def CataloguedForDel(self, cata):
        """
        删除编目功能验证
        marctyid:书目编号，定位要编目的书目记录
        :return: None
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/catalog/catalogue/delete', {
            'userToken': self.ep.getUserToken(),
            'marctyIds': cata
        }).json()
        if 'message' in res:
            if res['message'] == '操作成功!':
                print("删除编目成功")
            else:
                print("删除编目出错")
        else:
            print("删除编目出错", res)


if __name__ == '__main__':
    bianmu = CataloguedPage('TDJay', 'Td123456')
    bianmu.CataloguedForQuery()  # 编目管理书目列表功能验证
    cata = bianmu.CataloguedForAdd()  # 新增编目管理书目功能验证
    bianmu.CataloguedForMod(cata)  # 修改编目管理书目功能验证
    # bianmu.CataloguedForDel(cata)  # 删除编目管理书目功能验证
