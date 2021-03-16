# 作者       ：yangwuxie
# 创建时间   ：2020/9/3 15:50

"""
企微客户总览
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class EnterpriseCustomersOverview(unittest.TestCase):

    def test_enterpriseCustomersList(self):
        """
        企微客户总览列表
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase1", 1)

    def test_adjustPermissionCustomerList(self):
        """
        调整数据权限请求客户列表
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase2", 5)

    def test_customerChatIno(self):
        """
        代理人和客户聊天记录
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase3", 2)

    def test_queryUserWithUnexistName(self):
        """
        查询不存在的昵称
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase4", 1)

    def test_queryUserWithExistName(self):
        """
        查询存在的昵称
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase5", 1)

    def test_queryUserWithDepartId(self):
        """
        查询拾贝汇保机构
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase6", 1)

    def test_queryUserWithDepartIds(self):
        """
        查询多部门
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase7", 1)

    def test_queryUserWithWrongDepart(self):
        """
        查询不存在的部门
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase8", 1)

    def test_queryUserWithUserName(self):
        """
        查询员工姓名
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase9", 1)

    def test_queryUserWithWrongName(self):
        """
        查询不存在的员工
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase10", 1)

    def test_queryUserWithHighIntention(self):
        """
        查询高意向客户
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase11", 1)

    def test_queryUserWithSaleStage(self):
        """
        根据销售阶段筛选客户
        """
        api_send_check("/test_data/enterpriseCustomersOverview.yml", "testcase12", 1)


