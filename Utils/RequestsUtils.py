# -*- coding: utf-8 -*-”
import datetime
import requests
import random
import re

from urllib3 import encode_multipart_formdata

class RequestsPage:

    def __init__(self):
        self.re = requests
        self.rd = random
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/81.0.4044.138 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
        }

    def sendRequest(self, method, url, data=None):
        """
        发送 requests 不同类型的请求
        :param method: 请求方法(GET、POST)
        :param url: 请求地址(网址)
        :param data: 请求参数
        :return: req(<Response [200]>)
        """
        try:
            if method == "GET":
                return self.re.get(url=url, data=data, headers=self.headers)
            if method == "POST":
                return self.re.post(url=url, data=data, headers=self.headers)
            if method == "JSON":
                self.headers['Content-Type'] = 'application/json'
                return self.re.post(url=url, data=data, headers=self.headers)
            if method == "FILE":
                data['file'] = ('list.xls', open('D:\Cache\Project\TJProject\list.xls', 'rb').read())
                encode_data = encode_multipart_formdata(data)
                data = encode_data[0]
                self.headers['Content-Type'] = encode_data[1]
                return self.re.post(url=url, data=data, headers=self.headers, verify=False)
        except Exception as e:
            print(e)

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

    def randomValue(self, *args):
        """
        元祖中获取任意值
        :param args: Tuple
        :return: String
        """
        return self.rd.choice(*args)

    def matchNumber(self, str):
        """
        提取字符串中的数字（处理价格用）
        :param str: 处理的字符串
        :return: String
        """
        return re.compile(r'\d+').findall(str)[0]

    def matchString(self, listValue):
        """
        提取集合中的特定字符（处理著者用）
        :param listValue: List 值，包含集合
        :return:List
        """
        l = list()
        for fl in listValue:
            # print(fl)
            if fl['field'] == '701':
                a = re.findall(r"▼a(.+?)▼", fl['content'])
                if len(a) != 0:
                    l.append(a.pop())
                elif len(a) == 0:
                    b = re.findall(r"▼a(.+)", fl['content'])
                    l.append(b.pop())
                # 防止一本书有2条701，只取第一个
                break
        return l

    def modifyTuples(self, *args, value=4):
        """
        处理从数据库中提取出的元祖值，返回一个集合
        :param args: Tuple
        :param value: 默认取出数据库每一行的第5列，可以修改为其他列数
        :return: Set
        """
        s = set()
        for tup in args:
            if tup[value] != "":
                for t in tup[value].lstrip("{").rstrip("}").split(","):
                    s.add(t.strip().strip("'"))
        return s

    def nowTime(self, ty=None):
        """
        返回当前时间
        :param ty: 非必传，返回不同格式的时间；值为start/now
        :return:String
        """
        today = datetime.date.today()
        if ty == 'start':
            return today.replace(month=1, day=1)
        elif ty == 'end':
            return today + datetime.timedelta(days=1)
        else:
            return today

    def modifyNum(self, setValue):
        """
        统计所有书的借还续数量
        :param setValue: 传入一个集合，集合中的值为图书条码
        :return: List
        """
        cn1, cn2, cn3, cn4, cn5, cn6, cn7, cn8, cn9, cn10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        for cdv in setValue:
            # print(int(cdv[2:]))
            if 0 < int(cdv[2:]) < 101:
                cn1 += 1
            elif 100 < int(cdv[2:]) < 201:
                cn2 += 1
            elif 200 < int(cdv[2:]) < 301:
                cn3 += 1
            elif 300 < int(cdv[2:]) < 401:
                cn4 += 1
            elif 400 < int(cdv[2:]) < 501:
                cn5 += 1
            elif 500 < int(cdv[2:]) < 601:
                cn6 += 1
            elif 600 < int(cdv[2:]) < 701:
                cn7 += 1
            elif 700 < int(cdv[2:]) < 801:
                cn8 += 1
            elif 800 < int(cdv[2:]) < 901:
                cn9 += 1
            elif 900 < int(cdv[2:]) < 1001:
                cn10 += 1
        l = [cn1, cn2, cn3, cn4, cn5, cn6, cn7, cn8, cn9, cn10]
        # print(l)
        return l


if __name__ == '__main__':
    print(RequestsPage().nowTime())
    # a = ("adad", "asdad", "ssfg", "asfhsof")
    # print(RequestsPage().randomValue(a))
    # RequestsPage().modifyTuples((123, 'DZ04234', "{'TJ00591', 'TJ00432', 'TJ00002', 'TJ00009', 'TJ00311', 'TJ00571', 'TJ00275', 'TJ00558', 'TJ00447', 'TJ00243', 'TJ00096'}"))