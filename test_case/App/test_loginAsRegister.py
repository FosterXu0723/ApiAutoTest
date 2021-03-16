# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: yangwuxie
# Create Date: 2020-11-25
# Scenario:APP-注册即登录流程
#################################################
import requests
import json
import sys
import unittest
sys.path.append("../..")
from common.ReadConfig import *
from common.Log import *
from common.handle_yaml import *
from utils.Myddt import ddt, data, unpack
from common.Assert.Api_Send_check import *


getdata = HandleYaml('/test_data/loginAsRegister.yml').get_casename_step()
print (getdata)


@ddt
class LoginAsRegister(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_case(self, casename, caseno, step):
        result = api_send_check('/test_data/loginAsRegister.yml', caseno, step)


if __name__ == "__main__":
    unittest.main()
