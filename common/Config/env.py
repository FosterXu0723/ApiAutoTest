# @time   :2020/08/28
# @author : YiCai
import os
import sys


class Config(object):
    DEBUG = False

    def __getitem__(self, key):
        return self.__getattribute__(key)


class TEST(Config):
    APP_HOST = 'https://test.wxb.com.cn/substation'
    APP_MOBILE = '13390157984'
    MANAGER_HOST = ''
    MANAGER_USER = ''
    MANAGER_PASS = ''


class PRODUCT(Config):
    APP_HOST = 'https://test.wxb.com.cn/substation'
    APP_MOBILE = '13390157984'
    MANAGER_HOST = ''
    MANAGER_USER = ''
    MANAGER_PASS = ''


mapping = {
    'test': TEST,
    'product': PRODUCT,
    'default': TEST
}

# 根据脚本参数，来决定用那个环境配置


# print(sys.argv)
# num = len(sys.argv) - 1  # 参数个数
# if num < 1 or num > 1:
#     exit("参数错误,必须传环境变量!比如: python xx.py dev|pro|default")
# env = sys.argv[1]  # 环境
# print(env)


ENV = os.environ.get('ENV', 'test').lower()  # 设置为默认default
config = mapping[ENV]()
# print(config.APP_HOST)
