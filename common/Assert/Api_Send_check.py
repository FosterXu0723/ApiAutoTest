# -*- coding: utf-8 -*
# @time   :2020/08/02
# @author : YiCai
from common import ReqApi
from common.Assert import Assets
from common.Log import logger
import sys

sys.path.append("..")


def api_send_check(_path, case, steps):
    """
    接口请求并校验结果
    :param case: 单条用例 如testase1
    :param steps: 用例总共几步
    :param _path: case路径
    :return:
    """
    api = ReqApi.ReqApi(_path, case, steps)
    res = api.run_request()
    n = 2  # 大列表中几个数据组成一个小列表
    new_res = ([res[i:i + n] for i in range(0, len(res), n)])

    # print(new_res)
    if len(new_res) >= 1:
        for i, j in enumerate(new_res):
            Assets.Assert(case, i + 1, j[1], j[0], _path).check_result()
    else:
        logger.info('该用例下没有steps')


if __name__ == '__main__':
    path = '/test_case/Wakandahome/Login/test_agentEasyInfo.yml'
    path1 = '/test_data/agententry.yml'
    api_send_check(path1, 'testcase3', 2)
