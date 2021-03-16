# 作者       ：yangwuxie
# 创建时间   ：2020/11/17 15:47
"""
资产分配case
"""

import unittest

from common.Assert.Api_Send_check import api_send_check


class ResignUserManage(unittest.TestCase):

    def test_queryResignUser(self):
        """离职人员列表正常流程"""
        api_send_check('/test_data/resignUserManage.yml','testcase1',1)

    def test_queryResignUserWithNoneDate(self):
        """离职人员列表异常流程-不带日期"""
        api_send_check('/test_data/resignUserManage.yml', 'testcase2', 1)

    def test_queryTransferRecord(self):
        """客户分配记录列表，正常流程"""
        api_send_check('/test_data/resignUserManage.yml','testcase3', 1)

    def test_queryDepartTree(self):
        """查询组织架构树"""
        api_send_check('/test_data/resignUserManage.yml','testcase4', 1)

    def test_queryStaff(self):
        """查询员工"""
        api_send_check('/test_data/resignUserManage.yml', 'testcase5', 1)

    def test_queryNotExistStuff(self):
        """查询不存在的员工"""
        api_send_check('/test_data/resignUserManage.yml', 'testcase6', 1)

    def test_queryUserCustomer(self):
        """查询员工名下客户"""
        api_send_check('/test_data/resignUserManage.yml', 'testcase7', 2)

    def test_transferCustomer(self):
        """在职继承给本人-异常流程"""
        api_send_check('/test_data/resignUserManage.yml', 'testcase8', 2)