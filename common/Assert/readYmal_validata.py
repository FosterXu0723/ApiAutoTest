# @time   :2020/07/30
# @author : YiCai
# coding = utf-8
import os
import re
import json
import sys
from common.Log import logger
from common.handle_yaml import HandleYaml
from common.Assert.Get_Target_Value import get_target_value

sys.path.append("..")

global val


def read_yaml_val(testcase_no, step_no, path):
    """

    :param testcase_no: testcase1。。。
    :param step_no: step1 中的1  传入的是第几步的 具体数值 不是总步数
    :param path:
    :return:
    """
    steps = HandleYaml(path).get_casename_step()
    logger.info('{} 中的所有steps is \n                                                                {}'.format(path, steps))
    val_ = None
    # '测试数据yml {} 中没有目标用例 {} 或 目标用例 {} 中没有目标step {}'.format(path, testcase_no, testcase_no, step_no)
    ll = ''
    for i in steps:
        ll = ll + (''.join(get_target_value('caseno', i, [])))
    if testcase_no not in ll:
        logger.error('用例集中没有 {} 这个用例'.format(testcase_no))
    else:

        for i in steps:

            if testcase_no in i.values():
                all_step = i['step']
                if step_no in [i for i in range(1, all_step + 1)]:

                    # print('all step {}'.format(all_step))
                    res_ = HandleYaml(path).get_source(testcase_no, all_step)

                    step_no = step_no - 1
                    val_ = res_[step_no]
                else:
                    logger.error('{} 中没有步骤 {}'.format(testcase_no, step_no))

    return val_['validate']


if __name__ == '__main__':
    testDataDir = '/test_case/Wakandahome/Login/test_agentEasyInfo.yml'  # 这里用join 在win10下会有双斜杠的问题
    case = '/test_case/Wakandahome/Login/test_agentEasyInfo.yml'
    case1 = '/test_data/agententry.yml'
    case = case.replace('\\', '/')
    print('路径为 {}'.format(case1))
    print(read_yaml_val('testcase3', 2, case1))
