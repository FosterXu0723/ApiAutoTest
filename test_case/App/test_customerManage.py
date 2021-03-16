# 作者       ：yangwuxie
# 创建时间   ：2020/9/8 18:10

"""
客户管理
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class CustomerManage(unittest.TestCase):

    def test_queryfollowUpCustomer(self):
        """
        跟进客户
        """
        api_send_check("/test_data/customerManage.yml", "testcase1", 2)

    def test_queryDealCustomer(self):
        """
        成交客户
        """
        api_send_check("/test_data/customerManage.yml", "testcase2", 2)

    def test_holidayReminder(self):
        """
        节假日提醒
        """
        api_send_check("/test_data/customerManage.yml", "testcase3", 1)

    def test_customerCare(self):
        """
        客户关怀
        """
        api_send_check("/test_data/customerManage.yml", "testcase4", 1)

    def test_upsertCustomer(self):
        """
        新建跟进客户
        """
        api_send_check("/test_data/customerManage.yml", "testcase5", 3)

    def test_upsertCutomerFromCustomerDynamic(self):
        """获客动态新建跟进客户-删除"""
        api_send_check("/test_data/customerManage.yml", "testcase6", 3)