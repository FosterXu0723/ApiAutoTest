# 作者       ：yangwuxie
# 创建时间   ：2020/9/7 17:38

"""
敏感动作处理
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class SensitiveActionResolve(unittest.TestCase):

    def test_resolveSensitiveAction(self):
        """
        处理敏感动作-未处理列表
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase1", 1)

    def test_doneList(self):
        """
        已处理列表
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase2", 1)

    def test_getSensitiveByUserName(self):
        """
        按员工名称查询敏感动作列表
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase3", 1)

    def test_getSensitiveByCustomerName(self):
        """
        按好友名称查询敏感动作列表
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase4", 1)

    def test_getUndoSensitiveByTypeOne(self):
        """
        待处理列表-聊天涉及敏感词
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase5", 1)

    def test_getUndoSensitiveByTypeTwo(self):
        """
        待处理列表-撤回消息
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase6", 1)

    def test_getUndoSensitiveByTypeThree(self):
        """
        待处理列表-超时回复
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase7", 1)

    def test_getUndoSensitiveByTypeFour(self):
        """
        待处理列表-删除客户
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase8", 1)

    def test_getUndoSensitiveByTypeFive(self):
        """
        待处理列表-被客户删除
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase9", 1)

    def test_getDoneSensitiveByTypeOne(self):
        """
        已处理列表-聊天涉及敏感词
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase10", 1)


    def test_getDoneSensitiveByTypeTwo(self):
        """
        已处理列表-撤回消息
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase11", 1)

    def test_getDoneSensitiveByTypeThree(self):
        """
        已处理列表-超时回复
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase12", 1)

    def test_getDoneSensitiveByTypeFour(self):
        """
        已处理列表-删除客户
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase13", 1)

    def test_getDoneSensitiveByTypeFive(self):
        """
        已处理列表-被客户删除
        """
        api_send_check("/test_data/sensitiveActionResolve.yml", "testcase14", 1)
