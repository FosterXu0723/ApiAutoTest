# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-06-02
# Scenario:读取config.ini文件中的配置数据
#################################################
import os
import codecs
import configparser


class ReadConfig(object):
    proDir = os.path.split(os.path.dirname(__file__))[0]
    commonDir = os.path.dirname(os.path.realpath(__file__))
    configPath = os.path.join(commonDir, "../test_data/config.ini")
    testDataDir = os.path.join(os.path.split(commonDir)[0], "test_data")
    # 调用读取配置模块中的类
    conf = configparser.ConfigParser()
    # 读ini文件
    conf.read(configPath, encoding='utf-8')
    # 调用get方法，然后获取配置的数据
    log_file_name = conf.get('Log', 'file_name')
    log_console_level = conf.get('Log', 'console_output_level')
    log_file_output_level = conf.get('Log', 'file_output_level')
    log_pattern = None
    log_limit = conf.get('Log', 'backup')
    db_host = conf.get('DB', 'host')
    db_port = conf.get('DB', 'port')
    db_username = conf.get('DB', 'username')
    db_password = conf.get('DB', 'password')
    db_name = conf.get('DB', 'db_name')


if __name__ == '__main__':
    print(ReadConfig().proDir)
