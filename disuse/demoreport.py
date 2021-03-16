#coding=utf-8
import unittest
import os
import time
from BeautifulReport import BeautifulReport

#用例存放路径
case_paths=[os.path.join('../test_case/')]
#报告存放路径
#report_path = os.path.join('./test_report/')


def all_case():
    for case_path in case_paths:
        discover=unittest.defaultTestLoader.discover(case_path, pattern="test_demo.py", top_level_dir=None)
    return discover

if __name__ == '__main__':
    result = BeautifulReport(all_case())
    result.report(filename=u'demo自动化测试报告.html', description=u'接口调用自动化回归测试', report_dir='./test_report/')








# import unittest
# import HTMLTestRunnerNew
# import sys
# sys.path.append("..")
# from test_case.test_demo import DeomTest

# suite=unittest.TestSuite()
# loader=unittest.TestLoader()

# #加载
# suite.addTest(loader.loadTestsFromTestCase(DeomTest))

# #执行

# with open('TestReport.html','wb') as file:
#     runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2,title='test',description='金木0807',tester='金木')
#     runner.run(suite)