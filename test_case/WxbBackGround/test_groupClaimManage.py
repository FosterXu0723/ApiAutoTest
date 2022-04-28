# coding=utf-8
##################################################
# Copyright(c) 2021
# Environment: python 3.7
# Author By: zhanfei
# Create Date: 2021-12-16
# Scenario:喂小保后台---团险理赔管理
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

getdata = HandleYaml('/test_data/groupClaimManage.yml').get_casename_step()
print(getdata)


@ddt
class GroupClaimManage(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_case(self, casename, caseno, step):
        result = api_send_check('/test_data/groupClaimManage.yml', caseno, step)


if __name__ == "__main__":
    unittest.main()
