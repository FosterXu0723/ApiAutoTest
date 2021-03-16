# coding=utf-8
# @time   :2020/08/27
# @author : YiCai

from common.Assert import Api_Send_check
import unittest
from utils.Myddt import ddt, data, unpack
from common.handle_yaml import *
import os
import time
import os
import sys


module_name = str(os.path.basename(__file__)).split('.')[0]
path = r'/test_data/test_agentEasyInfo.yml'
get_data = HandleYaml(path).get_casename_step()
logger.info('用例 {}.py的测试驱动数据为: \n{}'.format(module_name, get_data))


@ddt
class agentEasyInfo(unittest.TestCase):
    @data(*get_data)
    @unpack
    def test_agentEasyInfo(self, casename, caseno, step):
        Api_Send_check.api_send_check(path, caseno,
                                      step)  # , {'Token': get_token()})
        time.sleep(0.1)


if __name__ == "__main__":
    # get_demotest1(),get_demotest2(),get_demotest3()
    # suite=unittest.TestSuite()
    # suite.addTest(DeomTest("test_f"))
    # runner=unittest.TextTestRunner(verbosity=2)
    # runner.run(suite())

    unittest.main()
