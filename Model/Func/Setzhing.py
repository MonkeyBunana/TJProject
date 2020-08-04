# -*- coding: utf-8 -*-
# @Time    : 2020/8/4 11:29
from Utils.ElibUtils import ElibPage
from Utils.RequestsUtils import RequestsPage


class SetzhingPage:

    def __init__(self):
        self.rp = RequestsPage()
        self.ep = ElibPage('zhouminhao', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D')

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


if __name__ == '__main__':
    SetzhingPage().BookmanForQuery()
