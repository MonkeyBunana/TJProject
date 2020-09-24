# -*- coding: utf-8 -*-”
import sqlite3
import json

class DBPage:

    def __init__(self, dbName):
        self.conn = sqlite3.connect('../'+dbName+'.db')
        self.cursor = self.conn.cursor()

    def createReader(self):
        try:
            sql = 'CREATE TABLE IF NOT EXISTS tb_reader(' \
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sex TEXT, dzdw TEXT, borrow TEXT, ' \
                    'return TEXT, now_bro INTEGER, bro INTEGER, ret INTEGER, ren INTEGER' \
                  ')'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()

    def createTotal(self):
        try:
            sql = 'CREATE TABLE IF NOT EXISTS tb_total(' \
                    'total_reader INTEGER, total_bro INTEGER, total_ret INTEGER, total_ren INTEGER, time TEXT' \
                  ')'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()

    def createBook(self):
        try:
            # 正题名 / 责任者 / ISBN / 出版社 / 著者（701a）/ 分类号 / 借阅次数 / 归还次数 / 续借次数
            sql = 'CREATE TABLE IF NOT EXISTS tb_book(' \
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, ztm TEXT, zrsm TEXT, isbn TEXT, cbs TEXT, zzm TEXT, ' \
                    'flh TEXT, bro INTEGER, ret INTEGER, ren INTEGER' \
                  ')'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()

    def addReader(self, list):
        try:
            sql = "INSERT INTO tb_reader(name, sex, dzdw, borrow, return, now_bro, bro, ret, ren) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cursor.executemany(sql, list)
            self.conn.commit()
        except Exception as e:
            print(e)
            # self.conn.rollback()

    def addTotal(self, list):
        try:
            sql = 'INSERT INTO tb_total(total_reader, total_bro, total_ret, total_ren, time) VALUES (?, ?, ?, ?, ?)'
            self.cursor.executemany(sql, list)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def addBook(self, list):
        try:
            sql = 'INSERT INTO tb_book(ztm, zrsm, isbn, cbs, zzm, flh, bro, ret, ren) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self.cursor.executemany(sql, list)
            self.conn.commit()
        except Exception as e:
            print(e)
            # self.conn.rollback()

    def updateReader(self, args):
        try:
            sql = 'UPDATE tb_reader SET name=?, sex=?, dzdw=?, borrow=?, return=?, now_bro=?, bro=?, ret=?, ren=? WHERE id=?'
            self.cursor.execute(sql, args)
            self.conn.commit()
        except Exception as e:
            print(e)
            # self.conn.rollback()

    def updateTotal(self, args):
        try:
            sql = 'UPDATE tb_total SET total_reader=?, total_bro=?, total_ret=?, total_ren=?, time=?'
            self.cursor.execute(sql, args)
            self.conn.commit()
        except Exception as e:
            print(e)
            # self.conn.rollback()

    def updateBook(self, args):
        try:
            sql = 'UPDATE tb_book SET ztm=?, zrsm=?, isbn=?, cbs=?, zzm=?, flh=?, bro=?, ret=?, ren=? WHERE id=?'
            self.cursor.execute(sql, args)
            self.conn.commit()
        except Exception as e:
            print(e)
            # self.conn.rollback()

    def selectReader(self):
        try:
            sql = 'SELECT * FROM tb_reader'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def selectReaderSex(self, value):
        try:
            sql = "SELECT bro, ren FROM tb_reader WHERE sex=?"
            self.cursor.execute(sql, [value])
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def selectReaderDzdw(self, value):
        try:
            sql = "SELECT bro, ret, sex, ren FROM tb_reader WHERE dzdw=?"
            self.cursor.execute(sql, [value])
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def selectReaderZzm(self, value):
        try:
            sql = "SELECT bro, ret FROM tb_book WHERE zzm=?"
            self.cursor.execute(sql, [value])
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def selectTotal(self):
        try:
            sql = 'SELECT * FROM tb_total'
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def selectBook(self):
        try:
            sql = 'SELECT * FROM tb_book'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def selectBookFlh(self, value):
        try:
            if value == '总计':
                sql = "SELECT bro, ret, ren FROM tb_book"
            else:
                sql = "SELECT bro, ret, ren FROM tb_book WHERE flh LIKE '"+value+"%'"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def deleteReader(self):
        try:
            sql = 'DELETE FROM tb_reader'
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def deleteTotal(self):
        try:
            sql = 'DELETE FROM tb_total'
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def deleteBook(self):
        try:
            sql = 'DELETE FROM tb_book'
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

if __name__ == '__main__':
    DBPage('book').createReader()
    DBPage('book').createTotal()
    DBPage('book').createBook()
    # a = [
    #     ('TJ1231', '{"1", "2", "3"}'),
    #     ('TJ4655', '{"4", "5"}')
    # ]
    # DBPage('book').addReader(a)
    # a = ('DZ06048', '{"7", "8", "9"}', 123)
    # DBPage('book').updateReader(a)
    # print(DBPage("book").selectReader())
    # print(DBPage('book').selectTotal())
    # DBPage('book').deleteReader()
    # print(DBPage('book').selectBookFlh('总计'))
    # print(DBPage('book').selectReaderZzm('张梦璐'))