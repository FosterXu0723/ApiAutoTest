# coding=utf-8
# @time   :2020/09/14
# @author : YiCai
import shutil
import os
import time
from common.Config.Global_Var import *


def remove_file(old_path, new_path):
    # print(old_path)
    # print(new_path)
    file_list = os.listdir(old_path)  # 列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    # print(file_list)
    # filename = os.listdir(old_path)[0]
    if len(file_list) != 0:
        print('将历史测试报告移动到old文件夹中')
        for file in file_list:
            src = os.path.join(old_path, file)
            dst = os.path.join(new_path, file)
            print('src:', src)
            print('dst:', dst)
            shutil.move(src, dst)

        src_name = "./test_report_old/接口调用自动化测试报告.html"
        des_name = "./test_report_old/接口调用自动化测试报告" + get_time('./common/Config/runtime.txt') + '.html'
        os.rename(src_name, des_name)
    else:
        print('test_report一个空文件夹，无需移动文件')


if __name__ == '__main__':
    # remove_file(r"../test_report", r"../test_report_old")
    filePath = r"../test_report"
    print(os.listdir(filePath)[0])
