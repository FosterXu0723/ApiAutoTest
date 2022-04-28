#  date:  2020/9/8
#  Author:  jinmu
#  Description:


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

getdata = HandleYaml('/test_data/InsureController_data/single_port_data/showConfirm_1.yml').get_casename_step()
print(getdata)


@ddt
class TestShowConfirm(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_showConfirm(self, casename, caseno, step):
        result = api_send_check('/test_data/InsureController_data/single_port_data/showConfirm_1.yml', caseno, step)


if __name__ == "__main__":
    unittest.main()