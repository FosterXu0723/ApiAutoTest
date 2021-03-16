# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-07-28
# Scenario:封装读取yaml文件方法
#################################################
import yaml
import json
import sys
import json

sys.path.append("..")
from common.Log import logger
from common.ReadConfig import ReadConfig
from utils.DataRandomUtils import *

import sys

sys.path.append("..")


class HandleYaml:

    def __init__(self, file_path=None):

        """
        os.path.abspath('.')表示获取当前文件所在目录;os.path.dirname表示获取文件所在父目录;所以整个就是项目的所在路径
        :param file_path:yaml文件路径,填写相对路径
        """
        root_dir = ReadConfig.proDir
        self.file_path = root_dir.replace('\\', '/') + file_path
        # self.file_path = os.path.join(root_dir, file_path)
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.yml = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"找不到文件{self.file_path}")

    def get_source(self, caseno=None, steps=None):

        """
        获得yaml文件中的单个用例数据
        :param caseno:用例编号
        :param steps:用例执行步数
        """
        try:
            d = self.yml[caseno]
        except KeyError:
            logger.error(f"当前数据：{self.yml} 中找不到{caseno}!!!")
        # d1=replace_params(d,paramsvalues)
        reqdatas = []
        """
        for中根据传入的执行步数，取每一步的数据作为一个字典,然后添加到reqdatas列表中
        步数从1开始计算,所以在传入的步数基础上加1
        """

        for num in range(1, int(steps) + 1):
            step = 'step' + str(num)
            reqdatas.append(d[step])
        return reqdatas

    def get_headersparamsvalue(self, caseno=None):
        """
        获得yaml文件中的单个用例headers中参数化的需要传入的实际值
        :param caseno:用例编号
        """
        try:
            d = self.yml[caseno]
            try:
                return d['headersparamsvalue']
            except KeyError:
                logger.warning("当前数据：{self.yml} 中找不到headersparamsvalue!!!")
                return None
        except KeyError:
            logger.error(f"当前数据：{self.yml} 中找不到{caseno}!!!")
            return self.yml

    def get_dataparamsvalue(self, caseno=None):
        """
        获得yaml文件中的单个用例data中参数化的需要传入的实际值
        :param caseno:用例编号
        """
        try:
            d = self.yml[caseno]
            try:
                return d['dataparamsvalue']
            except KeyError:
                logger.warning(f"当前数据：{self.yml} 中找不到dataparamsvalue!!!")
                return None
        except KeyError:
            logger.error(f"当前数据：{self.yml} 中找不到{caseno}!!!")
            return self.yml

    def get_casename_step(self):
        """
        从yaml文件中读取用例描述,用例编号,用例执行步数
        """
        casesteps = []
        for testcase in self.yml.keys():
            """
            data.keys(),从data中把用例编号全部取出,结果例如['testcase1', 'testcase2']
            """
            try:
                if self.yml[testcase]['Enabled'].upper() == "YES":
                    """
                    Enabled:YES为用例有效,NO为用例无效
                    """
                    stepcount = json.dumps(self.yml[testcase]).count("step")
                    """
                    先把data[testcase]转为字符串，然后统计每个case中step的数目，作为用例执行步数
                    """
                    case_step = {'casename': self.yml[testcase]['casename'], 'caseno': testcase, 'step': stepcount}
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
                logger.error("用例执行步数异常{}".format(e))

        return casesteps


if __name__ == '__main__':
    # test = HandleYaml('/test_case/Wakandahome/Login/test_agentEasyInfo.yml').get_source('testcase1', 1)
    # print(test)

    # test1 = HandleYaml('/test_data/demo.yml').get_source('testcase3', 2)
    # test2 = HandleYaml('/test_data/demo.yml').get_headersparamsvalue('testcase1')
    # test3 = HandleYaml('/test_case/Wakandahome/Login/test_agentEasyInfo.yml').get_dataparamsvalue('testcase1')

    # test4 = HandleYaml('/test_data/GetToken.yml').get_casename_step()
    # print(test1)[]

    test4 = HandleYaml('/test_data/agententry.yml').get_casename_step()
    #test5 = HandleYaml('/test_case/Wakandahome/Login/demo1.yml').get_source('testcase1', 2)
    print(test4)

