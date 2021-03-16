# 作者       ：yangwuxie
# 创建时间   ：2020/9/7 13:55

"""
敏感词配置流程
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class SensitiveConfiguration(unittest.TestCase):


    def test_configSensitive(self):
        """
        敏感词配置删除
        """
        api_send_check("/test_data/sensitiveWordConfiguration.yml", "testcase1", 4)
