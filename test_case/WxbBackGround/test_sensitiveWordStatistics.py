# 作者       ：yangwuxie
# 创建时间   ：2020/9/4 17:14
"""
敏感词统计列表
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class SensitiveWordStatistics(unittest.TestCase):

    def test_sensitive(self):
        """
        敏感词统计列表
        """
        api_send_check("/test_data/sensitiveWordStatistics.yml", "testcase1", 1)


