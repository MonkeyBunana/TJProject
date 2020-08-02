# -*- coding: utf-8 -*-”
# 读写txt，暂时已被废弃

class ReadPage:

    def __init__(self):
        pass

    def read(self):
        s = set()
        file_handle = open('../name.txt', mode='r')
        for line in file_handle.readlines():
            line = line.strip('\n')
            s.add(line)
        file_handle.close()
        return tuple(s)


    def write(self, args):
        file_handle = open('../name.txt', mode='w')
        file_handle.truncate()      # 清空再写入
        for n in args:
            file_handle.write(n+'\n')
        file_handle.close()


if __name__ == '__main__':
    a = ("ada", "asdada", "adadada", "dafaf", "asfda")
    ReadPage().write(a)
    print(ReadPage().read())