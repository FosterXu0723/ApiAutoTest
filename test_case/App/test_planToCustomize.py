# 作者       ：yangwuxie
# 创建时间   ：2020/8/27 11:23

"""
方案定制相关case
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class PlanToCustomize(unittest.TestCase):
    """
    方案定制
    """
    def test_planToCustomize(self):
        """
        APP-方案定制-方案定制正常流程
        :return:
        方案定制正常流程
        """
        api_send_check('/test_data/planToCustomize.yml', "testcase1", 2)

    def test_withoutFollowId(self):
        """
        APP-方案定制-请求详情不带方案定制id
        :return:
        请求详情不带方案定制id
        """
        api_send_check('/test_data/planToCustomize.yml', "testcase2", 2)

    def test_RiskAssessment(self):
        """
        保险方案定制风险测评报告
        """
        api_send_check('/test_data/planToCustomize.yml', "testcase3", 2)

