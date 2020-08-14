# -*- coding: utf-8 -*-
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage


class WebopacPage:

    def __init__(self, loginName, loginPwd):
        self.rp = RequestsPage()
        self.ep = ElibPage(loginName, loginPwd)

    def opacManage(self):
        print(self.simpleSearch())
        print(self.advanceSearch())
        print(self.opacReaderLogin())



    def simpleSearch(self, searchValue=None, searchItem='ztming', size=10, current=1, sortValue=0,
                     isBrwNum=0, haveCollection=1, sortField='cbYear', cbYear=None, cbYear2=None,
                     leixing=None, classify=None, category=None, subCategory=None):
        """ 检索首页
        :param searchValue: 搜索值
        :param searchItem:  搜索项，比如：
            任意词keyWord、题名ztming、ISBN/ISSNisbn、责任者zrsming、主题词zti、分类号flhao、
            订购号dghao、出版地cbdi、出版社cbzhe、从编seriesStatement、索书号sshao、统一书刊号unifyNumber
        :param size: 每页多少条数据，比如（10）
        :param current: 现在第几页，比如（1）
        :param sortValue: 排序，升序为0，降序为1
        :param isBrwNum: 借阅最多，1为勾选，0为未勾选
        :param haveCollection: 只显示在馆记录，1为勾选，0为未勾选
        :param sortField: 排序选项，比如：
            匹配度score、题名ztming、责任者zrsming、索书号sshao、出版社cbzhe、出版日期cbYear、馆藏数bookNum
        :param cbYear: 出版日期开始年，比如（2010）
        :param cbYear2: 出版日期结束年，比如（2011）
        :param leixing: 文献类型，比如：图书aa、期刊bb、其他other
        :param classify: 分类 第一层，比如（A）
        :param category: 分类 第二层，比如（A1）
        :param subCategory: 分类 第三层，比如（A12）
        :return: String 操作成功
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/p/search/advanceSearch', {
            'size': size,
            'current': current,
            searchItem: searchValue,
            'sortValue': sortValue,
            'isBrwNum': isBrwNum,
            'haveCollection': haveCollection,
            'sortField': sortField,
            'yzhong': '',       # 语种，但是中英文都是空值
            'libIds': self.ep.getLibid(),   # 馆id
            'cbYear': cbYear,
            'cbYear2': cbYear2,
            'leixing': leixing,
            'classify': classify,
            'category': category,
            'subCategory': subCategory
        }).json()
        if res['message'] == '操作成功':
            print(res['data']['page']['dataList'])
        else:
            print('查询失败')

    def advanceSearch(self, size=10, current=1, sortValue=0, isBrwNum=0, haveCollection=1, sortField='cbYear',
                      cbYear=None, cbYear2=None, leixing=None, classify=None, category=None, subCategory=None,
                      searchField1='ztming', searchField2='ztming', searchField3='ztming', searchValue1=None,
                      searchValue2=None, searchValue3=None, assemblyType1='or', assemblyType2='or'):
        """ 高级检索
        :param size: 每页多少条数据，比如（10）
        :param current: 现在第几页，比如（1）
        :param sortValue: 排序，升序为0，降序为1
        :param isBrwNum: 借阅最多，1为勾选，0为未勾选
        :param haveCollection: 只显示在馆记录，1为勾选，0为未勾选
        :param sortField: 排序选项，比如：
            匹配度score、题名ztming、责任者zrsming、索书号sshao、出版社cbzhe、出版日期cbYear、馆藏数bookNum
        :param cbYear: 出版日期开始年，比如（2010）
        :param cbYear2: 出版日期结束年，比如（2011）
        :param leixing: 文献类型，比如：图书aa、期刊bb、其他other
        :param classify: 分类 第一层，比如（A）
        :param category: 分类 第二层，比如（A1）
        :param subCategory: 分类 第三层，比如（A12）
        :param searchField1: 搜索项
        :param searchField2: 搜索项
        :param searchField3: 搜索项
            任意词keyWord、题名ztming、ISBN/ISSNisbn、责任者zrsming、主题词zti、分类号flhao、
            订购号dghao、出版地cbdi、出版社cbzhe、从编seriesStatement、索书号sshao、统一书刊号unifyNumber
        :param searchValue1: 搜索值
        :param searchValue2: 搜索值
        :param searchValue3: 搜索值
        :param assemblyType1: or / and
        :param assemblyType2: or / and
        :return: String
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/p/search/advanceSearch', {
            'size': size,
            'current': current,
            'classify': classify,
            'category': category,
            'subCategory': subCategory,
            'sortValue': sortValue,
            'isBrwNum': isBrwNum,
            'haveCollection': haveCollection,
            'sortField': sortField,
            'yzhong': '',   # 语种
            'libIds': self.ep.getLibid(),
            'cbYear': cbYear,
            'cbYear2': cbYear2,
            'leixing': leixing,
            'searchField1': searchField1,
            'searchField2': searchField2,
            'searchField3': searchField3,
            'searchValue1': searchValue1,
            'searchValue2': searchValue2,
            'searchValue3': searchValue3,
            'assemblyType1': assemblyType1,
            'assemblyType2': assemblyType2
        }).json()
        if res['message'] == '操作成功':
            print(res['data']['page']['dataList'])
        else:
            print('查询失败')

    def opacReaderLogin(self):
        # 获取读者token
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/p/login/readerLogin', {
            'loginName': self.ep.getReaderList()['data']['dataList'][0]['dzzhao'],
            'loginPwd': self.ep.getReaderList()['data']['dataList'][0]['mima']
        }).json()
        # 获取读者信息
        r1 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/opac/reader/barcode', {
            'readerToken': res['data']['readerToken']
        }).json()
        r2 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/opac/book/list/nowcheckout', {
            'readerToken': res['data']['readerToken']
        }).json()
        print(r1)


if __name__ == '__main__':
    print(WebopacPage('cwq', '84548081').opacManage())