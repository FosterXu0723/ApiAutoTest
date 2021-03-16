# 作者       ：yangwuxie
# 创建时间   ：2020/9/29 16:19

"""
方案定制管理
"""
import unittest

from common.Assert.Api_Send_check import api_send_check


class SchemaMakeVersionManage(unittest.TestCase):

    def test_querySchemeVersion(self):
        """方案定制列表"""
        api_send_check("./test_data/schemaMakeVersionManage.yml", "testcase1", 1)

    def test_querySchemeVersionWithWrongName(self):
        """用不存在的方案名查询方案定制列表"""
        api_send_check("./test_data/schemaMakeVersionManage.yml", "testcase2", 1)

    def test_editSchemeVersion(self):
        """编辑方案名称，保存方案定制信息"""
        api_send_check("./test_data/schemaMakeVersionManage.yml", "testcase3", 2)

    def test_querySchemeVersionWithExistName(self):
        """按存在的方案名称查询方案定制链接"""
        api_send_check("./test_data/schemaMakeVersionManage.yml", "testcase4", 1)

    def test_editSchemeVersionWithoutName(self):
        """编辑方案定制名称为空，保存"""
        api_send_check("./test_data/schemaMakeVersionManage.yml", "testcase5", 2)

    def test_updateAgentVersion(self):
        """设置为代理人版本（app中展示）"""
        api_send_check("./test_data/schemaMakeVersionManage.yml", "testcase6", 2)