# -*- coding: utf-8 -*-”
# -*- coding: utf-8 -*-”
import xlrd

class ExcelPage:

    def __init__(self, excelName):
        # 获取Excel表路径
        self.excel_path = 'D:\Cache\Project\TJProject\%s' % excelName
        # 获取Excel用例表
        self.excel_sheet = 'Sheet1'
        # 打开Excel
        self.data = xlrd.open_workbook(self.excel_path)
        # 打开指定用例表
        self.table = self.data.sheet_by_name(self.excel_sheet)
        # 获取有效行数
        self.rowNum = self.table.nrows
        # 获取有效列数
        self.colNum = self.table.ncols
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        self.keys = self.table.row_values(0)

    def read_excel(self):
        """ 读取数据，并返回一个 list，数据包装成 dict
            PS：xlrd的数据类型有：0 empty, 1 string, 2 number, 3 date, 4 boolean, 5 error
               数字一律按浮点型输出，日期输出成一串小数，布尔型输出0或1，所以我们必须在程序中做判断处理转换成我们想要的数据类型
        :return: List
        """
        # 定义一个空列表
        datas = []
        for i in range(1, self.rowNum):
            # 定义一个空字典
            sheet_data = {}
            for j in range(self.colNum):
                # 获取单元格数据类型
                c_type = self.table.cell(i, j).ctype
                # 获取单元格数据
                c_cell = self.table.cell_value(i, j)
                if c_type == 2 and c_cell % 1 == 0:    # 如果是整形
                    c_cell = int(c_cell)
                sheet_data[self.keys[j]] = c_cell
            datas.append(sheet_data)
        return datas



if __name__ == "__main__":
    print(ExcelPage('番禺区教育局成员馆部分用户登录信息.xls').read_excel())
