# -*- coding: utf-8 -*-”
from sys import _getframe

class ExceptionPage(Exception):

    def __init__(self, clsName, defName, exceptionMsg):
        self.clsName = clsName
        self.defName = defName
        self.exceptionMsg = exceptionMsg

    def __str__(self):
        return '-------------------------------------- \n' \
               '位置：' + self.clsName + ' -> ' + self.defName + '() \n' \
               '错误信息：' + self.exceptionMsg + ' \n' \
               '--------------------------------------'

    def ErrorTemplate(self, jsonData, searchData, isMore):
        if jsonData['code'] == 0:
            # data 存在于 response 中
            if 'data' in jsonData:
                # dataList 存在于 response 中
                if 'dataList' in jsonData['data']:
                        # dataList 长度不为0
                        if len(jsonData['data']['dataList']) != 0:
                            templateList = list()
                            for tl in jsonData['data']['dataList']:
                                templateList.append(tl[searchData])
                            if isMore is True:
                                return tuple(templateList)
                            else:
                                return tuple(templateList)[0]
                            # return jsonData['data']['dataList'][0]['yslxid']
                        else:
                            raise ExceptionPage(
                                _getframe().f_code.co_filename,
                                _getframe().f_code.co_name,
                                searchData + ' 缺少默认值'
                            )
                else:
                    if len(jsonData['data']) != 0:
                        templateList = list()
                        for tl in jsonData['data']:
                            templateList.append(tl[searchData])
                        if isMore is True:
                            return tuple(templateList)
                        else:
                            return tuple(templateList)[0]
                    else:
                        raise ExceptionPage(
                            _getframe().f_code.co_filename,
                            _getframe().f_code.co_name,
                            searchData + ' dataList 字段找不到'
                        )
            else:
                    raise ExceptionPage(
                        _getframe().f_code.co_filename,
                        _getframe().f_code.co_name,
                        searchData + ' data 字段找不到'
                    )
        else:
            raise ExceptionPage(
                _getframe().f_code.co_filename,
                _getframe().f_code.co_name,
                jsonData['message']
            )
