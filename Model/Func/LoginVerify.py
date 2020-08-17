# -*- coding: utf-8 -*-
import multiprocessing
import time
from Utils.ExcelUtils import ExcelPage
from Utils.ElibUtils import ElibPage

class LoginVerifyPage:

    def __init__(self):
        # 创建进程池，cpu核心数为2
        self.pool = multiprocessing.Pool(processes=2)



    def multiLogin(self, excelName):
        """
        多进程运行登录程序
        :param excelName: 测试的excel文件
        :return:
        """
        start = time.time()
        for i in ExcelPage(excelName).read_excel():
            self.pool.apply_async(self.logincheck(str(i['用户名']), str(i['密码']), str(i['成员馆'])))
        self.pool.close()
        self.pool.join()
        print(f"time: {round(time.time() - start, 3)}")       # 输出所用的时间

    def logincheck(self, zh, mm, g):
        res = ElibPage(zh, mm).msg
        if res['message'] == '操作成功':
            if res['data']['user']['libName'] == g:
                print(g + " 的账户：" + res['data']['user']['username'] + " 登录成功")
                return "登录成功"
            else:
                print("用户登录的成员馆：" + res['data']['user']['libName'] + " 和excel中的成员馆：" + g + " 不符")
                return "登录失败"
        else:
            print(g + " 中的账户：" + zh + " 提示 " + res['message'])
            return "登录失败"


if __name__ == "__main__":
    LoginVerifyPage().multiLogin('测试登录信息.xls')
