# 作者       ：yangwuxie
# 创建时间   ：2020/9/1 15:18
import unittest

from common.Assert.Api_Send_check import api_send_check
import sys
sys.path.append("../..")


class WeWorkChat(unittest.TestCase):

    def test_serviceInfo(self):
        """
        企微客户总览概况
        :return:
        """
        api_send_check('/test_data/weWorkChat.yml', "testcase1", 2)

    def test_chatInfo(self):
        """
        企微聊天记录
        :return:
        """
        api_send_check('/test_data/weWorkChat.yml','testcase2',2)

    def test_queryStaff(self):
        """
        查询统计单元
        :return:
        """
        api_send_check('/test_data/weWorkChat.yml', "testcase3", 1)

    def test_queryStaffWithWrongName(self):
        """
        查询不存在的统计单元
        :return:
        """
        api_send_check('/test_data/weWorkChat.yml', "testcase4", 1)



