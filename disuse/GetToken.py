# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-06-02
# Scenario:通过登录接口获取Token
#################################################
import requests
import json
import sys

sys.path.append("..")
from common.ReadConfig import *
from common.Log import *
from common.ReqApi import *

log = Log().get_logger()


# 调用获取token接口
def get_token():
    rmt = ReqApi('/test_data/GetToken.yml', 'testcase1', 2)
    result = rmt.run_request()
    data2 = result[2]
    print (data2)
    token = data2['data']['token']
    return token


if __name__ == "__main__":
    print(get_token())
