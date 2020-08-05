# -*- coding: utf-8 -*-”
import base64
from urllib import parse
from Crypto.Cipher import AES


class AesPage:

    def __init__(self):
        self.key = 'www.tuodielib.cn'
        self.MODE = AES.MODE_ECB
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    # str不是16的倍数那就补足为16的倍数
    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    def AES_encrypt(self, text):
        aes = AES.new(AesPage.add_to_16(self.key), self.MODE)  # 初始化加密器
        # 执行加密并转码返回bytes
        encrypted_text = str(base64.encodebytes(aes.encrypt(AesPage.add_to_16(self.pad(str(text))))), encoding='utf-8').replace('\n', '')  # 这个replace大家可以先不用，然后在调试出来的结果中看是否有'\n'换行符
        # python3对于url的编码
        return parse.quote(encrypted_text)

if __name__ == '__main__':
    print(AesPage().AES_encrypt("123456"))