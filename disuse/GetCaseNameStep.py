# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-08-07
# Scenario:封装从yaml文件中读取用例描述,用例编号,用例执行步数
#################################################
import yaml
import os
import jsonpath
import sys
import json

# sys.path.append("..")
from common.Log import logger


class GetCaseNameStep:
    """
    :param file_path:yaml文件路径,填写相对路径
    """

    def __init__(self, file_path=None):
        # os.path.abspath('.')表示获取当前文件所在目录;os.path.dirname表示获取文件所在父目录;所以整个就是项目的所在路径
        # root_dir = os.path.dirname(os.path.abspath('.'))
        root_dir = os.path.abspath(os.path.dirname(__file__)).split('ApiAutoTest')[0] + 'ApiAutoTest'
        self.file_path = root_dir.replace('\\', '/') + file_path

    def get_casename_step(self):
        """
        从yaml文件中读取用例描述,用例编号,用例执行步数
        """
        fp = None
        casesteps = []
        try:
            fp = open(self.file_path, encoding='utf-8')
            data = yaml.safe_load(fp)
        except FileNotFoundError:
            logger.error(f"文件{self.file_path}不存在，请检查文件路径是否正确")
        for testcase in data.keys():
            """
            data.keys(),从data中把用例编号全部取出,结果例如['testcase1', 'testcase2']
            """
            try:

                if data[testcase]['Enabled'].upper() == "YES":
                    """
                    Enabled:YES为用例有效,NO为用例无效
                    """
                    stepcount = json.dumps(data[testcase]).count("step")
                    """
                    先把data[testcase]转为字符串，然后统计每个case中step的数目，作为用例执行步数
                    """
                    case_step = {'casename': data[testcase]['casename'], 'caseno': testcase, 'step': stepcount}
                    """
                    case_step:包含了单个用例的用例描述,用例编号,用例执行步数
                    """
                    casesteps.append(case_step)
                    """
                    casesteps:包含了一个yaml中所有用例的用例描述,用例编号,用例执行步数,把单个用例的结果加入到列表中
                    """
                else:
                    pass
            except Exception as e:
                logger.error("用例编号{}取用例描述,用例执行步数异常".format(testcase))

        return casesteps


if __name__ == '__main__':

    test = GetCaseNameStep('/test_case/Wakandahome/Login/test_agentEasyInfo.yml').get_casename_step()
    # test_1 = GetCaseNameStep('/test_case/Wakandahome/Login/test_agentEasyInfo.yml').get_casename_step()

    test = GetCaseNameStep('/test_data/GetToken.yml').get_casename_step()

    print(test)
