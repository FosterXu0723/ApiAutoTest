# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-07-16
# Scenario:批量执行case
#################################################
import operator
import pickle
import unittest
import os
import time
from BeautifulReport import BeautifulReport
from tomorrow import threads
from utils.remove import remove_file
from common.Log import logger
from common.Config.Global_Var import *
import shelve
from utils.DingTalkRobot import remindFailure

# 用例存放路径



#case_paths = [os.path.dirname('./test_case/App/'),os.path.join('./test_case/Supplychain/'),os.path.join('./test_case/WxbBackGround/'),os.path.join('./test_case/Supplychain/InsureController/')]
#case_paths = [os.path.dirname('./test_case/Supplychain/InsureController/')]




case_paths = [os.path.dirname('./test_case/App/'), os.path.join('./test_case/Supplychain/'),
              os.path.join('./test_case/WxbBackGround/'), os.path.join('./test_case/Supplychain/InsureController/'), os.path.join('./test_case/Supplychain/Prospectus/'), os.path.join('./test_case/Supplychain/mhb/'),os.path.join('./test_case/Supplychain/employerInsurance/'),os.path.join('./test_case/GroupInsurPlatForm/')]


def all_case():
    testcases = unittest.TestSuite()
    for case_path in case_paths:
        TL = unittest.TestLoader()
        discovers = TL.discover(case_path, pattern="test*.py", top_level_dir=None)
        testcases.addTests(discovers)
    return testcases


class Serialization(BeautifulReport):

    """
    统计历史执行结果
    """

    def __init__(self, suites):
        super().__init__(suites)
        self.suites = suites
        self.allPassFlag = True

    def _getTestResultList(self):
        super().report(filename=u'接口调用自动化测试报告.html', description=u'接口调用自动化回归测试', report_dir='./test_report/')
        return self.result_list

    def historyRunResult(self, target):
        """
        [{"className":"","methodName":"","caseDescript":"","failTotal":"","passTotal":"","passRate":""}]
        :param target:
        :return:
        """
        # if not os.path.exists(target):
        #     os.mkdir(path=target)
        testReulstList = self._getTestResultList()
        if os.path.exists(target) and os.path.getsize(target) > 0:
            with open(target, "rb") as file:
                historyResult = pickle.load(file)
                testMethodList = self._getReulstMethodName(historyResult)
                for caseReult in testReulstList:
                    try:
                        index = testMethodList.index(caseReult[0] + caseReult[1])
                        if operator.contains(caseReult[4], "成功"):
                            historyResult[index]["passTotal"] = historyResult[index]["passTotal"] + 1
                        else:
                            if operator.contains(caseReult[4], "失败"):
                                self.allPassFlag = False
                            historyResult[index]["failTotal"] = historyResult[index]["failTotal"] + 1
                        historyResult[index]["passRate"] = historyResult[index]["passTotal"] / (
                                historyResult[index]["failTotal"] + historyResult[index]["passTotal"]
                        )
                    except Exception:  # 新增的case
                        passTotal = failTotal = 0
                        if operator.contains(caseReult[4], "成功"):
                            passTotal += 1
                        else:
                            if operator.contains(caseReult[4], "失败"):
                                self.allPassFlag = False
                            failTotal += 1
                        try:
                            passRate = passTotal / (passTotal + failTotal)
                        except Exception:  # 处理结果不是正常
                            passRate = 0
                        historyResult.append({"className": caseReult[0],
                                              "methodName": caseReult[1],
                                              "caseDescript": caseReult[2],
                                              "failTotal": failTotal,
                                              "passTotal": passTotal,
                                              "passRate": passRate})

            print(historyResult)
            with open(target, "wb") as f:  # 写入file
                pickle.dump(historyResult, f)
        else:
            historyResult = []
            for caseReult in testReulstList:
                passTotal = failTotal = 0
                if operator.contains(caseReult[4], "成功"):
                    passTotal += 1
                else:
                    if operator.contains(caseReult[4], "失败"):
                        self.allPassFlag = False
                    failTotal += 1
                try:
                    passRate = passTotal / (passTotal + failTotal)
                except Exception:
                    passRate = 0
                caseDict = {"className": caseReult[0],
                            "methodName": caseReult[1],
                            "caseDescript": caseReult[2],
                            "failTotal": failTotal,
                            "passTotal": passTotal,
                            "passRate": passRate}
                historyResult.append(caseDict)
            print(historyResult)
            with open(target, 'wb') as f:
                pickle.dump(historyResult, f)
        if not self.allPassFlag:
            remindFailure()

    def _getReulstMethodName(self, testResultList):
        """
        统一标识某一个
        :param testResultList:
        :return:
        """
        methodNameList = []
        for result in testResultList:
            methodNameList.append(result["className"] + result["methodName"])
        return methodNameList


@threads(20)
def run(test_suit):
    t1 = time.time()
    result = Serialization(test_suit)

    result.historyRunResult("./test_report/historyResult")
    t2 = time.time()
    print('运行时间为 {}'.format(t2 - t1))


if __name__ == '__main__':
    # 1.获取当前时间,这样便于下面的使用.
    # now=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 2.html报告文件路径
    # report_abspath=os.path.join(report_path, "result_"+now+".html")
    # report_abspath=os.path.join(report_path, "H5回调自动化测试报告.html")
    # 3.打开一个文件,将result写入此file中
    # fp=open(report_abspath, "w",encoding='utf-8')
    # runner=HTMLTestRunner(stream=fp,title=u'H5回调自动化测试报告,测试结果如下:',description=u'用例执行情况:')
    # 4.调用add_case函数返回值
    # runner.run(all_case())
    # result = BeautifulReport(all_case())
    # result.report(filename=u'接口调用自动化测试报告.html', description=u'接口调用自动化回归测试', report_dir='./test_report/')
    # print(result.result_list)
    # fp.close()
    # serialization = Serialization(all_case())
    # serialization.historyRunResult(r"C:\Users\Administrator\PycharmProjects\ApiAutoTest\test_report\historyResult")
    # t1 = time.time()
    # result = BeautifulReport(all_case())
    # result.report(filename=u'接口调用自动化测试报告' + time.strftime(' %Y-%m-%d %H点%M分%S秒'.encode('unicode_escape').decode('utf8'),
    #                                                       time.localtime(time.time())).encode('utf-8').decode(
    #     'unicode_escape') + '.html',
    #               description=u'接口调用自动化回归测试', report_dir='./test_report/')
    # t2 = time.time()
    # print('运行时间为 {}'.format(t2 - t1))


    
    # remove_file("./test_report", "./test_report_old")
    cases = all_case()
    run(cases)
    # save_time('./common/Config/runtime.txt')
