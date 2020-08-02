# -*- coding: utf-8 -*-
from Utils.RequestsUtils import RequestsPage
from Utils.ElibUtils import ElibPage

class InterviewPage:

    def __init__(self):
        self.rp = RequestsPage()
        self.ep = ElibPage('TJ', '6Tet8CNiT2soE8BiYcXR%2FA%3D%3D')

    def subscriptionBooksImport(self):
        return self.rp.sendRequest('POSTFILE', self.ep.getUrl() + '/service/api/e/interview/file/zdsmI', {
            'Content-Disposition:form-data; name="excel"; filename="征订书目列表.xls" Content-Type:application/vnd.ms-excel': '<file>',
            'Content-Disposition:form-data;name="userToken"': self.ep.getUserToken()
        })


if __name__ == '__main__':
    print(InterviewPage().subscriptionBooksImport())