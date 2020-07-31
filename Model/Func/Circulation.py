# -*- coding: utf-8 -*-
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage


class CirculationPage:

    def __init__(self, loginName, loginPwd):
        self.rp = RequestsPage()

        self.baseUrl = "http://192.168.1.120:8080"
        self.msg = ElibPage().getLoginMsg(self.baseUrl+'/service/api/p/login/userLogin', loginName, loginPwd)
        print(self.msg)

    def ReaderManage(self):
        pass

    def DocumentCirculation_Bro(self):
        

if __name__ == '__main__':
    CirculationPage('pysyzx', '123456')