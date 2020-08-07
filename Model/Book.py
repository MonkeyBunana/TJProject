# -*- coding: utf-8 -*-”
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage
from Utils.SqlLiteUtils import DBPage
import random

class Book:

    def __init__(self):
        self.rp = RequestsPage()
        self.ep = ElibPage('TJ', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D')
        self.slp = DBPage('book')

    def copyBooks(self, num):
        """ 编目-回溯建库
        此方法用于给每书目添加馆藏
        :param num: 每个书目添加多少馆藏（填写100那么每本书添加100条馆藏数据）
        :return: 无返回
        """
        # 保存图书信息的 list
        l = list()
        # 馆藏信息中的条码号，用于循环递增
        count = 0
        # 发送 requests 请求，获取书目信息（这是一个 json 值）
        res_1 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/catalog/catalogue/list', {
            'userToken': self.ep.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'libId': self.ep.getLibid(),
            'userType': 1,
            'dateType': 1
        }).json()
        # 循环 requests 返回的书目信息，处理数据
        for dataList in res_1['data']['dataList']:
            # 处理返回值，获取 著者 字段
            fl = self.rp.matchString(dataList['fieldList'])
            # 处理没有 著者 字段的图书，返回一个空值
            if len(fl) == 0:
                fl = ['']
            # 添加信息到 list 中
            l.append((
                dataList['ztming'],
                dataList['zrsming'],
                dataList['isbn'],
                dataList['cbzhe'],
                fl[0],
                dataList['flhao'],
                0,
                0,
                0
            ))
            # 循环值，判断什么时候跳出while循环
            loopValue = 0
            while True:
                # 循环次数递增
                loopValue += 1
                # 条码递增
                count += 1
                # 发送 requests 请求，给每本书一条条添加馆藏
                self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/book/save', {
                    'ztai': '在馆',
                    'tiaoma': 'TJ'+str(count).zfill(5),
                    'bookCodes': 'TJ'+str(count).zfill(5),
                    'sshao': dataList['flhao']+'/1',
                    'gysid': self.ep.getGysid(),
                    'batchid': self.rp.randomValue(self.ep.getBatchid()),
                    'ltlxid': self.ep.getLtlxid(),
                    'cygid1': self.ep.getLibid(),
                    'cygid0': self.ep.getLibid(),
                    'ysuanid': self.ep.getYslxid(),
                    'marctyId': dataList['marctyid'],
                    'cejia': self.rp.matchNumber(dataList['jge']),
                    'taojia': self.rp.matchNumber(dataList['jge']),
                    'userToken': self.ep.getUserToken(),
                    'czid0': self.rp.randomValue(self.ep.getCzid()),
                    'czid1': self.rp.randomValue(self.ep.getCzid()),
                    'bookNum': 1,
                    'purchasePrice': '',
                    'purchaseDiscount': '',
                    'jcmshu': '',
                    'beizhu': '',
                    'sellPrice': '',
                    'wxlyuan': '',
                    'jzleixing': '',
                    'zdfangshi': '',
                    'sellDiscount': ''
                }).json()
                # 控制什么时候跳出死循环，每本书目添加 num 本馆藏后跳出，添加下一本
                if loopValue >= num:
                    break
        # 更新数据，将图书信息添加到 tb_book 数据库中
        self.slp.addBook(l)

    def borrowBooks(self):
        """ 流通-借还管理-借出
        此方法用于给读者随机借书
        :return:无返回
        """
        # 将所有图书条码添加到集合中，检查所有添加的条码是否重复
        checkDoubleValue = set()
        # 将每个用户借的图书条码添加到集合中，获取单个用户接了哪几本书
        temp_bro = set()
        # 获取 tb_total 表的数据
        tb = self.slp.selectTotal()
        # 获取 tb_reader 表的数据
        selectData = self.slp.selectReader()
        for tup_1 in selectData:
            # 将数据库中所有用户的条码添加到集合中查重，防止多次运行借书数据库数据与业务系统对不上
            checkDoubleValue = checkDoubleValue | self.rp.modifyTuples(tup_1)

        for tup_2 in selectData:
            # 循环值，判断什么时候跳出while循环
            loopValue = 0
            # 获取随机借书数量（每个人借多少本）
            a = random.randint(1, 20)
            # 将个人之前借的书添加到集合中
            temp_bro = temp_bro | self.rp.modifyTuples(tup_2)
            while True:
                # 获取随机图书条码
                randomValue = 'TJ' + str(random.randint(1, 1000)).zfill(5)
                # 对比图书条码是否已在数据库中存在，存在就不发送借书请求
                if randomValue in checkDoubleValue:
                    print('获取随机图书已重复')
                else:
                    # 发送借书请求
                    self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/bro', {
                        'userToken': self.ep.getUserToken(),
                        'readerBarcode': tup_2[1],
                        'bookBarcode': randomValue
                    })
                    # 所有图书集合 / 个人图书集合添加图书
                    checkDoubleValue.add(randomValue)
                    temp_bro.add(randomValue)
                    # 循环次数自增
                    loopValue += 1
                    # 当循环次数大于等于个人借书随机数，跳出循环
                    if loopValue >= a:
                        # 更新数据，将读者信息更新到 tb_reader 数据库中
                        self.slp.updateReader((
                            tup_2[1],
                            tup_2[2],
                            tup_2[3],
                            str(temp_bro),
                            tup_2[5],
                            int(tup_2[6]+len(temp_bro)),
                            int(tup_2[7]+len(temp_bro)),
                            tup_2[8],
                            tup_2[9],
                            tup_2[0]
                        ))
                        # 清空个人借书集合，防止插入数据库值错误
                        temp_bro.clear()
                        break

        # 处理数据获取借阅数量，返回值是一个 list
        t = self.rp.modifyNum(checkDoubleValue)
        # 用于 list 下标递增
        lv = 0
        for tup_3 in self.slp.selectBook():
            # 更新数据，将图书信息更新到 tb_book 数据库中
            self.slp.updateBook((
                tup_3[1],
                tup_3[2],
                tup_3[3],
                tup_3[4],
                tup_3[5],
                tup_3[6],
                t[lv],
                tup_3[8],
                tup_3[9],
                tup_3[0]
            ))
            # 下标递增
            lv += 1
        # 更新数据，将统计信息更新到 tb_total 数据库中
        self.slp.updateTotal((
            tb[0],
            int(tb[1]) + len(checkDoubleValue),
            tb[2],
            tb[3],
            str(self.rp.nowTime())
        ))


    def returnBooks(self):
        """ 流通-借还管理-归还
        此方法用于给读者随机还书
        :return:无返回
        """
        # 获取 tb_total 表的数据
        tb = self.slp.selectTotal()
        # 好像没用，但是懒得删，怕爆炸 :)
        count = 0
        # temp_bro 用于存放借出图书；temp_ret 用于存放还回图书，循环一次会清空
        temp_bro = set()
        temp_ret = set()
        # temp_bro_all 用于存放借出图书；temp_ret_all 用于存放还回图书，不会清空
        temp_bro_all = set()
        temp_ret_all = set()
        # 循环从数据库中取出的 tb_reader 表信息
        for tup in self.slp.selectReader():
            # 获取数据库中用户借的图书条码，添加到集合中
            temp_bro = temp_bro | self.rp.modifyTuples(tup)
            # 如果借出是空的，就不发送借书请求，更新 tb_reader 数据库
            if len(temp_bro) == 0:
                self.slp.updateReader((
                    tup[1],
                    tup[2],
                    tup[3],
                    "",
                    tup[5],
                    len(temp_bro),
                    tup[7],
                    int(tup[8])-len(temp_bro),
                    tup[9],
                    tup[0]
                ))
            else:
                # 获取还书随机值
                loopValue = random.randint(1, len(temp_bro))
                while loopValue > 0:
                    # 好像没软用，不敢删 :)
                    count += 1
                    # 获取集合中的任意一个条码
                    temp = temp_bro.pop()
                    # 将还回条码添加到还回集合中
                    temp_ret.add(temp)
                    # 发送 requests 请求，用户还书
                    self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/ret', {
                        'userToken': self.ep.getUserToken(),
                        'isSameCz': '1',
                        'bookBarcode': temp
                    })
                    # 递减到0退出循环
                    loopValue -= 1
                # 数据库中借书为空时运行程序容易把set()插入数据库中，做下处理
                # 如果借书为空，传空字符串
                if str(temp_bro) == 'set()':
                    self.slp.updateReader((
                        tup[1],
                        tup[2],
                        tup[3],
                        '',
                        str(temp_ret),
                        len(temp_bro),
                        tup[7],
                        int(tup[7]) - len(temp_bro),
                        tup[9],
                        tup[0]
                    ))
                # 借书不为空，就把信息更新到 tb_reader 数据库中
                else:
                    self.slp.updateReader((
                        tup[1],
                        tup[2],
                        tup[3],
                        str(temp_bro),
                        str(temp_ret),
                        len(temp_bro),
                        tup[7],
                        int(tup[7]) - len(temp_bro),
                        tup[9],
                        tup[0]
                    ))
            # 将每个人的借/还书添加到一个集合中
            temp_bro_all = temp_bro_all | temp_bro
            temp_ret_all = temp_ret_all | temp_ret
            # 清空集合，防止程序错误
            temp_bro.clear()
            temp_ret.clear()
        # 处理数据，获取各图书的还数量
        tba = self.rp.modifyNum(temp_bro_all)
        tra = self.rp.modifyNum(temp_ret_all)
        # 用于 list 下标递增
        lv = 0
        # 更新数据，将图书信息更新到 tb_book 数据库中
        for tup_3 in self.slp.selectBook():
            self.slp.updateBook((
                tup_3[1],
                tup_3[2],
                tup_3[3],
                tup_3[4],
                tup_3[5],
                tup_3[6],
                tba[lv],
                tra[lv],
                tup_3[9],
                tup_3[0]
            ))
            # 下标递增
            lv += 1
        # 更新数据，将统计信息更新到 tb_total 数据库中
        self.slp.updateTotal((
            tb[0],
            tb[1],
            tb[2] + count,
            tb[3],
            str(self.rp.nowTime())
        ))

    def renewBooks(self):
        """ 流通-借还管理-续借
        此方法用于给读者随机续借
        :return:无返回
        """
        # 保存每个用户借阅的图书
        temp = set()
        # 所有用户借阅的图书
        tenp_all = set()
        # 统计数据用
        count = 0
        # 获取 tb_total 表的数据
        tb = self.slp.selectTotal()
        # 循环从数据库中取出的 tb_reader 表信息
        for tup in self.slp.selectReader():
            # 循环值，判断什么时候跳出while循环
            loopValue = 1
            # 获取数据库中用户借的图书条码，添加到集合中
            temp = temp | self.rp.modifyTuples(tup)
            # print(temp)
            # 空的不处理
            if len(temp) != 0:
                # 获取续借随机值(每个用户续借多少本)
                a = random.randint(1, len(temp))
                while a >= loopValue:
                    # 获取set中的任意值
                    t = temp.pop()
                    # 将所有续借条码添加到集合中
                    tenp_all.add(t)
                    count += 1
                    # 发送 requests 请求，用户续借
                    self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/ren', {
                        'userToken': self.ep.getUserToken(),
                        'readerBarcode': tup[1],
                        'bookBarcode': t
                    })
                    loopValue += 1
                # 更新数据，将统计信息更新到 tb_reader 数据库中
                self.slp.updateReader((
                    tup[1],
                    tup[2],
                    tup[3],
                    tup[4],
                    tup[5],
                    tup[6],
                    tup[7],
                    tup[8],
                    a,
                    tup[0]
                ))
                temp.clear()
        # 处理数据，获取各图书的续借数量
        t = self.rp.modifyNum(tenp_all)
        # 用于 list 下标递增
        lv = 0
        # 更新数据，将图书信息更新到 tb_book 数据库中
        for tup_3 in self.slp.selectBook():
            self.slp.updateBook((
                tup_3[1],
                tup_3[2],
                tup_3[3],
                tup_3[4],
                tup_3[5],
                tup_3[6],
                tup_3[7],
                tup_3[8],
                t[lv],
                tup_3[0]
            ))
            # 下标递增
            lv += 1
        # 更新数据，将统计信息更新到 tb_total 数据库中
        self.slp.updateTotal((
            tb[0],
            tb[1],
            tb[2],
            tb[3] + count,
            str(self.rp.nowTime())
        ))

    def allReturnBooks(self):
        """ 流通-借还管理-归还
        此方法用于给读者全部归还
        :return:无返回
        """
        # 发送 requests 请求，用户归还条码1~1000的图书
        for n in range(1, 1001):
            self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/flow/doclx/ret', {
                'userToken': self.ep.getUserToken(),
                'isSameCz': '1',
                'bookBarcode': 'TJ' + str(n).zfill(5)
            })

    def clearBooks(self):
        """ 流通-借还管理-归还
        此方法用于清除所有馆藏图书
        :return:无返回
        """
        # 用于存储馆藏书目的id
        l = list()
        # 清空前先把书都还了
        self.allReturnBooks()
        # 发送 requests 请求，获取书目信息，返回 json 值
        res_1 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/catalog/catalogue/list', {
            'userToken': self.ep.getUserToken(),
            'pageNumber': 1,
            'pageSize': 50,
            'libId': self.ep.getLibid(),
            'userType': 1,
            'dateType': 1
        }).json()
        # 处理数据
        for dataList in res_1['data']['dataList']:
            # 发送 requests 请求，获取馆藏信息，返回 json 值
            res_2 = self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/book/listByCatalogue', {
                'userToken': self.ep.getUserToken(),
                'marctyId': dataList['marctyid'],
                'pageSize': 1000,
                'pageNumber': 1,
                'isShow': 0
            }).json()
            for r in res_2['data']['page']['dataList']:
                # 将要删除的馆藏 id 添加到列表中
                l.append(r['shuceid'])
        # 发送 requests 请求，删除馆藏信息，返回 json 值
        self.rp.sendRequest('POST', self.ep.getUrl() + '/service/api/e/book/delete', {
            'userToken': self.ep.getUserToken(),
            'shuceIds': ','.join(l)
        }).json()
        self.slp.deleteTotal()
        self.slp.deleteBook()


if __name__ == '__main__':
    # Book().copyBooks(100)
    # Book().allReturnBooks()
    Book().renewBooks()
    # Book().borrowBooks()
    # Book().returnBooks()
    # Book().total()
    # Book().clearBooks()