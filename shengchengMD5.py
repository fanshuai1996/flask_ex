#coding=utf8

import  hashlib

def sheng_md5(str):
    a=hashlib.md5()
    a.update(str.encode('utf8'))
    return a.hexdigest()


if __name__ == '__main__':
    str='sadasdsadasdsad'
    a=sheng_md5(str)
    print(a)

