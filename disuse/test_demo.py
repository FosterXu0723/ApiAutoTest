# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-07-28
# Scenario:代理人入职场景
#################################################
import requests
import json
import sys
import unittest
sys.path.append("..")
from common.ReadConfig import *
from common.Log import *
from common.ReqApi import *
from common.handle_yaml import *
# from ddt import ddt,data,unpack
from utils.Myddt import ddt, data, unpack
from common.Assert.Api_Send_check import *


# def get_demotest1():
# 	rmt=ReqApi('/test_data/demo2.yaml','testcase1',1,{'Token':get_token()})
# 	result=rmt.run_request()
# 	print (result)

# # def get_demotest2():
# # 	rmt=ReqApi('/test_data/demo2.yaml','testcase2',2,{'Token':get_token()})
# # 	result=rmt.run_request()
# # 	print (result)

# # def get_demotest3():
# # 	rmt=ReqApi('/test_data/demo2.yaml','testcase3',2,{'Token':get_token()})
# # 	result=rmt.run_request()
# # 	print (result)
# # # 	
# # 	
# test_data=cs().hm(5)
# a=GetCaseNameStep('/test_data/demo1.yaml').get_casename_step()
getdata = HandleYaml('/test_data/agententry.yml').get_casename_step()
print (getdata)


@ddt
class DeomTest(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_f(self, casename, caseno, step):
        rmt = api_send_check('/test_data/agententry.yml', caseno, step)


if __name__ == "__main__":
    # get_demotest1(),get_demotest2(),get_demotest3()
    # suite=unittest.TestSuite()
    # suite.addTest(DeomTest("test_f"))
    # runner=unittest.TextTestRunner(verbosity=2)
    # runner.run(suite())

    unittest.main()
