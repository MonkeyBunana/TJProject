# -*- coding: utf-8 -*-
from Utils.ElibUtils import ElibPage
from Utils.ExcelUtils import ExcelPage

from Model.Func.Circulation import CirculationPage
from Model.Func.Interview import InterviewPage
from Model.Func.Webopac import WebopacPage

class LoginVerifyPage:

    def __init__(self):
        pass

    def logincheck(self, excelName):
        for i in ExcelPage(excelName).read_excel():
            zh = str(i['用户名'])
            mm = str(i['密码'])
            g = str(i['成员馆'])
            try:
                res = ElibPage(zh, mm).getLoginMsg()
                if res['message'] == '操作成功':
                    if res['data']['user']['libName'] == g:
                        print()
                        print(g + " 的账户：" + res['data']['user']['username'] + " 登录成功")
                        print("--------------- 其他测试开始 ---------------")
                        print(CirculationPage(zh, mm).BRRManage())
                        print(InterviewPage(zh, mm).ZDManage())
                        print(WebopacPage(zh, mm).opacManage())
                        print("--------------- 其他测试结束 ---------------")
                        print()
                    else:
                        print("用户登录的成员馆：" + res['data']['user']['libName'] + " 和excel中的成员馆：" + g + " 不符")
                else:
                    print(g + " 中的账户：" + zh + " 提示 " + res['message'])
            except Exception as e:
                print(e)

if __name__ == "__main__":
    LoginVerifyPage().logincheck('番禺区教育局当前有借阅的成员馆登录信息(1).xls')