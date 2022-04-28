# coding=utf-8
##################################################
# Copyright(c) 2021
# Environment: python 3.7
# Author By: zhanfei
# Create Date: 2021-09-13
# Scenario:企团险平台--代理人管理
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

getdata = HandleYaml('/test_data/GroupInsurPlatForm_data/agentGroupManage.yml').get_casename_step()
print(getdata)


@ddt
class AgentGroupManage(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_case(self, casename, caseno, step):
        result = api_send_check('/test_data/GroupInsurPlatForm_data/agentGroupManage.yml', caseno, step)


if __name__ == "__main__":
    unittest.main()
