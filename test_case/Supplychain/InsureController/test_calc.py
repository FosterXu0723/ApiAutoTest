#  date:  2020/9/3
#  Author:  jinmu
#  Description:  详情页单被保人算价接口

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

getdata = HandleYaml('/test_data/InsureController_data/single_port_data/calc.yml').get_casename_step()
print(getdata)


@ddt
class TestCalc(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_calc(self, casename, caseno, step):
        result = api_send_check('/test_data/InsureController_data/single_port_data/calc.yml', caseno, step)


if __name__ == "__main__":
    unittest.main()