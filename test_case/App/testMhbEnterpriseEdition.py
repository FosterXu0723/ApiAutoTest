"""
@File:testMhbEnterpriseEdition.py
@author:yangwuxie
@date: 2021/02/01
"""

import unittest

from common.Assert.Api_Send_check import api_send_check


class MhbEnterprise(unittest.TestCase):
    # 民惠保入口关闭，此条case作废
    pass

    # def testPushOrder(self):
    #     """
    #     正常流程
    #     """
    #     api_send_check('/test_data/mhbEnterprise.yml', 'testcase1', 1)
    #
    # def testPushOrderWithoutCompanyName(self):
    #     """
    #     异常流程-没有携带企业名称，此流程还是能够走通
    #     """
    #     api_send_check('/test_data/mhbEnterprise.yml', 'testcase2', 1)
    #
    # def testPushOrderWithoutCompanyContactName(self):
    #     """
    #     异常流程，没有携带联系人信息，接口拦截异常请求
    #     """
    #     api_send_check('/test_data/mhbEnterprise.yml', 'testcase3', 1)
    #
    # def testPushOrderWithoutCompanyTel(self):
    #     """
    #     异常流程-没有携带企业联系方式，接口拦截异常请求
    #     """
    #     api_send_check('/test_data/mhbEnterprise.yml', 'testcase4', 1)
