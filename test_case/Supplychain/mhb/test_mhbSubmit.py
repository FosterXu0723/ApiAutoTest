#  date:  2021/2/4
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

getdata = HandleYaml('/test_data/InsureController_data/mhb/mhbSubmit.yml').get_casename_step()
print(getdata)


@ddt
class TestMhbSubmit(unittest.TestCase):
    @data(*getdata)
    @unpack
    def test_mhbSubmit(self, casename, caseno, step):
        result = api_send_check('/test_data/InsureController_data/mhb/mhbSubmit.yml', caseno, step)


if __name__ == "__main__":
    unittest.main()