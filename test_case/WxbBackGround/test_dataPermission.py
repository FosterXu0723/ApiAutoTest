# 作者       ：yangwuxie
# 创建时间   ：2020/10/27 17:14

import unittest

from common.Assert.Api_Send_check import api_send_check


class DataPermission(unittest.TestCase):

    def test_allPermission(self):
        "修改拥有全部数据权限"
        api_send_check("/test_data/dataPermission.yml",'testcase1',2)