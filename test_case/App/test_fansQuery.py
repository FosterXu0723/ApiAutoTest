# 作者       ：yangwuxie
# 创建时间   ：2020/8/25 15:15
import os
import unittest

from common.Assert.Api_Send_check import api_send_check
from common.ReadConfig import ReadConfig


class FansQuery(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_query(self):
        """APP-粉丝查询-粉丝查询流程"""
        api_send_check('/test_data/fansQuery.yml', "testcase1", 1)

    def test_queryWithoutNickname(self):
        """粉丝查询异常：不带昵称"""
        api_send_check('/test_data/fansQuery.yml', "testcase2", 1)

    def test_queryWithWrongNickname(self):
        """粉丝查询异常：带错误的昵称信息"""
    def test_query_without_nickname(self):
        """APP-粉丝查询-粉丝查询异常:不带昵称"""
        api_send_check('/test_data/fansQuery.yml', "testcase2", 1)

    def test_query_with_wrong_nickname(self):
        """APP-粉丝查询-粉丝查询异常:带错误的昵称信息"""
        api_send_check('/test_data/fansQuery.yml', "testcase3", 1)

    def tearDown(self) -> None:
        pass
