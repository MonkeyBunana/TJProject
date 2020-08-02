# -*- coding: utf-8 -*-”
import unittest
from Model.Book import Book
from Model.Reader import Reader
from Utils.SqlLiteUtils import DBPage
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage

class LTTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(LTTest, self).__init__(*args, **kwargs)
        self.book = Book()
        self.reader = Reader()
        self.db = DBPage('book')
        self.rp = RequestsPage()
        self.ep = ElibPage('TJ', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D')

    def test_lttj_default(self):
        """ 流通-流通统计
        获取总计数据 与 tb_total的借/还数 进行比较
        :return:
        """
        # TODO: 1. 增加每本图书藏址到数据库中  2. 增加对藏址图书统计的测试
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/lttjList', {
                'userToken': self.ep.getUserToken(),
                'type': 1,
                'cygid0': self.ep.getLibid(),
                'cygid1': self.ep.getLibid(),
                'timeType': 1,
                'pageSize': 50,
                'pageNumber': 1
        }).json()
        self.assertEqual(res['data']['dataList'][0]['list2'][0]['jccs'], str(self.db.selectTotal()[1]))
        self.assertEqual(res['data']['dataList'][0]['list2'][0]['ghcs'], str(self.db.selectTotal()[2]))

    def test_ltxd_default(self):
        """ 流通-流通详单
        获取总的数据数量 与 tb_total的借/还/续相加 进行比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/ltxd', {
            'userToken': self.ep.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'libId': self.ep.getLibid()
        }).json()
        result = self.db.selectTotal()[1] + self.db.selectTotal()[2] + self.db.selectTotal()[3]
        self.assertEqual(res['data']['totalElements'], str(result))

    def test_ltxd_search_readerId(self):
        """ 流通-流通详单
        查询每个读者的借/还/续总量 与 tb_reader的读者借/还/续相加 进行比较
        :return:
        """
        for data in self.db.selectReader():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/ltxd', {
                'userToken': self.ep.getUserToken(),
                'pageNumber': 1,
                'pageSize': 50,
                'libId': self.ep.getLibid(),
                'dzzhao': data[1]
            }).json()
            self.assertEqual(res['data']['totalElements'], str(data[7]+data[8]+data[9]))

    def test_ltxd_search_title(self):
        """ 流通-流通详单
        查询每本书的借/还/续总量 与 tb_book的图书借/还/续相加 进行比较
        PS：由于tb_book中的借数量是减掉了还的数量，所以统计时还的数量应该为2倍
        :return:
        """
        for data in self.db.selectBook():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/ltxd', {
                'userToken': self.ep.getUserToken(),
                'pageNumber': 1,
                'pageSize': 50,
                'libId': self.ep.getLibid(),
                'ztming': data[1]
            }).json()
            self.assertEqual(res['data']['totalElements'], str(data[7]+data[8]*2+data[9]))

    def test_dzjyphb_default(self):
        """ 流通-读者借阅排行榜
        查询每个读者的总借阅册次 与 tb_reader的读者总借阅册次 进行比较
        :return:
        """
        for data in self.db.selectReader():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/dzjyphb', {
                'userToken': self.ep.getUserToken(),
                'libid': self.ep.getLibid(),
                'renshu': 100,
                'pageNumber': 1,
                'pageSize': 50,
                'jycs': 1,
                'dzzhao': data[1]
            }).json()
            self.assertEqual(res['data']['dataList'][0]['jieyuecs'], data[7] + data[9])

    def test_dzjhtj_default(self):
        """ 流通-读者借还统计
        查询每个读者的借/还/续次数 与 tb_reader的借/还/续次数 进行比较
        :return:
        """
        for data in self.db.selectReader():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/dzjhtj', {
                'userToken': self.ep.getUserToken(),
                'libid': self.ep.getLibid(),
                'pageNumber': 1,
                'pageSize': 50,
                'dzzhao': data[1]
            }).json()
            self.assertEqual(res['data']['page']['dataList'][0]['jieyuecs'], data[7] + data[9])
            self.assertEqual(res['data']['page']['dataList'][0]['guihuancs'], data[8])
            self.assertEqual(res['data']['page']['dataList'][0]['xujiecs'], data[9])

    def test_wxjyphb_default(self):
        """ 流通-文献借阅排行榜
        查询每本书的总借阅册次 与 tb_book的读者总借阅册次 进行比较
        :return:
        """
        for data in self.db.selectBook():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/wxjyphb', {
                'userToken': self.ep.getUserToken(),
                'libid': self.ep.getLibid(),
                'renshu': 100,
                'pageNumber': 1,
                'pageSize': 50,
                'jycs': 1,
                'ztming': data[1]
            }).json()
            print(data)
            print(res['data']['dataList'][0])
            for r in res['data']['dataList']:
                if r['ztming'] == data[1]:
                    self.assertEqual(res['data']['dataList'][0]['jieyuecs'], data[7]+data[8])

    def test_wxjhtj_default(self):
        """ 流通-文献借还统计
        查询每个大类的借阅册次 与 tb_book的每个书目挑选相关类型相加 进行比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/wxjhtj', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid()
        }).json()
        for data in res['data']:
            val = 0
            for d in self.db.selectBookFlh(data['wxlx']):
                val = val + d[0] + d[1] + d[2]
            self.assertEqual(data['jycs'], str(val))

    def test_dzlxjhtj_default(self):
        """ 流通-读者类型借还统计
        因为只有一个读者类型，所以直接和 tb_total 的借阅数/归还数进行比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/dzlxjhtj', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 15
        }).json()
        for data in res['data']['dataList']:
            self.assertEqual(data['jieyuecs'], self.db.selectTotal()[1] + self.db.selectTotal()[3])
            self.assertEqual(data['guihuancs'], self.db.selectTotal()[2])

    def test_dzdwjhtj_default(self):
        """ 流通-读者单位借还统计
        根据数据库中读者的读者单位全部相加 进行比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/dzdwjhtj', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 15
        }).json()
        for data in res['data']['dataList']:
            val_bro, val_ret = 0, 0
            for d in self.db.selectReaderDzdw(data['dzdw']):
                val_bro = val_bro + d[0] + d[3]
                val_ret = val_ret + d[1]
            self.assertEqual(data['jieyuecs'], val_bro)
            self.assertEqual(data['guihuancs'], val_ret)

    def test_zzph_default(self):
        """ 流通-著者排行
        根据数据库中书目的著者比较借阅次数
        PS：借阅次数在还书方法中减掉了还书次数，所以完整的借阅次数应该为借阅次数+归还次数
        :return:
        """
        for data in self.db.selectBook():
            if data[5] == '':
                break
            else:
                res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/authorRank', {
                    'userToken': self.ep.getUserToken(),
                    'libId': self.ep.getLibid(),
                    'pageNumber': 1,
                    'pageSize': 50,
                    'equalType': 1,
                    'brwNum': 1,
                    'rankNum': 100,
                    'author': data[5]
                }).json()
            self.assertEqual(res['data']['dataList'][0]['brwNum'], str(data[7]+data[8]))

    def test_dzbqjhtj_defaul(self):
        """ 流通-读者标签借还统计
        根据 selectReaderDzdw 方法，会返回读者借/还/性别的元祖，根据性别将借/还相添加比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/readerLabelCir', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        for data in res['data']['dataList']:
            bro_num, ret_num = 0, 0
            for d in self.db.selectReaderDzdw(data['readerUnit']):
                if d[2] == data['readerGenderName']:
                    bro_num = bro_num + d[0] + d[3]
                    ret_num = ret_num + d[1]
            self.assertEqual(data['brwNum'], bro_num)
            self.assertEqual(data['returnNum'], ret_num)

    def test_dzxbjytj_defaul(self):
        """ 流通-读者性别借阅统计
        根据 selectReaderSex 方法，会返回读者借/续的元祖，将借/续相添加比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/readerGenderBorrowList', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'statisticalPeriod': 0,
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        num_1, num_2, man_num, famale_num = 0, 0, 0, 0
        for data in res['data']['dataList']:
            man_num = man_num + int(data['manBorrwoNumber'])
            famale_num = famale_num + int(data['femaleBorrowNumber'])
        for mNum in self.db.selectReaderSex('男'):
            num_1 = num_1 + mNum[0] + mNum[1]
        for fNum in self.db.selectReaderSex('女'):
            num_2 = num_2 + fNum[0] + fNum[1]
        self.assertEqual(num_1, man_num)
        self.assertEqual(num_2, famale_num)

    def test_dzxbjytj_total(self):
        """ 流通-读者性别借阅统计
        由于测试时合计小于月数量，故将月数量循环相加与合计相比较
        :return:
        """
        res_1 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/readerGenderBorrowList', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'statisticalPeriod': 0,
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        res_2 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/totalGenderBorrow', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        man_num, famale_num = 0, 0
        for data in res_1['data']['dataList']:
            print(data)
            man_num = man_num + int(data['manBorrwoNumber'])
            famale_num = famale_num + int(data['femaleBorrowNumber'])
        print(res_2['data'])
        self.assertEqual(man_num, res_2['data']['manBorrow'])
        self.assertEqual(famale_num, res_2['data']['femaleBorrow'])

    def test_jysktj_default(self):
        """ 流通-借阅时刻统计
        获取合计数量和数据库 tb_book 借阅/续借相比较
        :return:
        """
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/timeBorrowList', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'date1': self.rp.nowTime('start'),
            'date2': self.rp.nowTime('end'),
            'time1': '00',
            'time2': '00'
        }).json()
        data = self.db.selectTotal()
        self.assertEqual(res['data']['totalBorrow'][0], data[1] + data[3])

    def test_jysktj_total(self):
        """ 流通-借阅时刻统计
        获取合计数量和各个时间段 相比较
        :return:
        """
        num = 0
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/lttj/timeBorrowList', {
            'userToken': self.ep.getUserToken(),
            'libId': self.ep.getLibid(),
            'date1': self.rp.nowTime('start'),
            'date2': self.rp.nowTime('end'),
            'time1': '00',
            'time2': '00'
        }).json()
        for data in res['data']['hourList']:
            num = num + int(data['borrowNumber'])
        self.assertEqual(res['data']['totalBorrow'][0], num)

    def test_dzdqjycx_default(self):
        """ 流通-读者当前借阅查询
        每本书进行搜索，搜索的到就ok
        :return:
        """
        for data in self.db.selectReader():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/ltcx/dzjycx', {
                'userToken': self.ep.getUserToken(),
                'libid': self.ep.getLibid(),
                'dzzhao': data[1],
                'pageNumber': 1,
                'pageSize': 50
            }).json()
            num = 0
            for d in res['data']['dataList']:
                num += 1
                if d['tiaoma'] in data[4]:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            self.assertEqual(num, len(self.rp.modifyTuples(data)))

    def test_dzdqjycx_total(self):
        """ 流通-读者当前借阅查询
        计算每个用户图书的数量，和总量进行比较
        :return:
        """
        num = 0
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/ltcx/dzjycx', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        for data in self.db.selectReader():
            num = num + len(self.rp.modifyTuples(data))
        self.assertEqual(num, int(res['data']['totalElements']))

    def test_dzlsjycx_default(self):
        """ 流通-读者历史借阅查询
        每本书进行搜索，搜索的到就ok
        :return:
        """
        for data in self.db.selectReader():
            res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/ltcx/dzjylscx', {
                'userToken': self.ep.getUserToken(),
                'libid': self.ep.getLibid(),
                'dzzhao': data[1],
                'pageNumber': 1,
                'pageSize': 50
            }).json()
            print(res)
            num = 0
            for d in res['data']['dataList']:
                num += 1
                if d['tiaoma'] in data[5]:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            self.assertEqual(num, len(self.rp.modifyTuples(data, value=5)))

    def test_dzlsjycx_total(self):
        """ 流通-读者历史借阅查询
        计算每个用户图书的数量，和总量进行比较
        :return:
        """
        num = 0
        res = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/ltcx/dzjylscx', {
            'userToken': self.ep.getUserToken(),
            'libid': self.ep.getLibid(),
            'pageNumber': 1,
            'pageSize': 50
        }).json()
        for data in self.db.selectReader():
            num = num + len(self.rp.modifyTuples(data, value=5))
        self.assertEqual(num, int(res['data']['totalElements']))


if __name__ == '__main__':
    unittest.main()