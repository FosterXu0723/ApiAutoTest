# coding=utf-8
##################################################
# Copyright(c) 2020
# Environment: python 3.5
# Author By: zhanfei
# Create Date: 2020-07-28
# Scenario:封装requests请求方法
#################################################
import requests
import json
import sys

sys.path.append("..")
import os

from common.Log import logger
from common.handle_yaml import *
from utils.ParamsUtils import *
from utils.DataRandomUtils import *
from utils.FunctionUtils import is_args_contains_function, process_function
from utils.GetParamBySequenceCall import GetParamBySequenceCall


# from common.GetToken import *


class ReqApi:
    def __init__(self, file_path=None, caseno=None, steps=None):

        """
        :param file_path:yaml文件路径,填写相对路径
        :param caseno:用例编号
        :param steps:用例执行步数
        :param headersparamsvalues:用例中header中参数化需要替换的实际值
        :param dataparamsvalues:用例中data中参数化需要替换的实际值
        """
        self.file_path = file_path
        self.caseno = caseno
        self.steps = steps
        self.yml_data = HandleYaml(self.file_path)
        self.headersparamsvalues = self.yml_data.get_headersparamsvalue(self.caseno)
        self.dataparamsvalues = self.yml_data.get_dataparamsvalue(self.caseno)
        if is_args_contains_function(self.headersparamsvalues):
            self.headersparamsvalues = process_function(self.headersparamsvalues)
        self.dataparamsvalues = self.yml_data.get_dataparamsvalue(self.caseno)
        if is_args_contains_function(self.dataparamsvalues):
            self.dataparamsvalues = process_function(self.dataparamsvalues)

    def get_datasource(self):
        """
        获得单个用例的所有数据
        """
        self.source = self.yml_data.get_source(self.caseno, self.steps)
        return self.source

    def pre_request(self, header, data):
        if is_args_contains_function(header):
            header = process_function(header)
        if is_args_contains_function(data):
            data = process_function(data)
        if is_params_need_handle(header):
            header = replace_params(header, self.headersparamsvalues)
            if is_params_need_handle(header):
                header = replace_params(header, global_vars)
        if is_params_need_handle(data):
            data = replace_params(data, self.dataparamsvalues)
            if is_params_need_handle(data):
                data = replace_params(data, global_vars)
        return header, data

    def pre_host(self, host):
        if is_args_contains_function(host):
            host = process_function(host)
        return host

    def run_request(self):

        """
        :param h3:从前面接口返回报文中取出后面接口header中参数化的实际值
        :param d3:从前面接口返回报文中取出后面接口data中参数化的实际值
        """
        self.get_datasource()
        self.respo = []
        # self.h3 = {}
        # self.d3 = {}
        for data in self.source:
            # host = data['general']['host']
            # host = self.pre_host(host)
            host = get_app_host()
            url = data['general']['path']
            if 'wxb' not in url:
                url = host + data['general']['path']

            method = data['general']['method']
            header = data["headers"]
            pay_load = data['data']
            if header and (method.lower() == "post") and (header['Content-Type'] != 'application/json'):
                if 'setparam' in data:
                    if data['setparam'] is not None:
                        nn=GetParamBySequenceCall().get_params(data['setname'],data['setparam'])
                        global_vars.update(nn)
                else:
                    pass
                header, request_data = self.pre_request(header, pay_load)

                try:
                    logger.info("********************开始执行请求********************")
                    logger.info('请求头部为 ：{}'.format(header))
                    logger.info('请求方法为 ：{}'.format(method))
                    logger.info('请求路径为 ：{}'.format(url))
                    logger.info('请求数据为 ：{}'.format(request_data))
                    requests.packages.urllib3.disable_warnings()
                    rs = requests.post(url=url, data=request_data, headers=header, verify=False)
                    logger.info(f"接口请求成功,响应为：{rs.text}")
                except Exception as e:
                    logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{request_data}\n接口请求头：{header}\n"
                                 f"接口响应状态码：{rs.status_code}\n错误信息：{e}")
                resp = json.loads(rs.text)
                http_code = rs.status_code
                if data['extract'] is not None:
                    """
                    self.h3.update()根据待提取的字段,提取响应报文中待提取字段实际值,并添加到h3字典中
                    self.d3.update()根据待提取的字段,提取响应报文中待提取字段实际值,并添加到d3字典中
                    """
                    eval_jsonpath_str(json.loads(rs.text), data['extract'])
                self.respo.append(resp)
                self.respo.append(http_code)

            elif header and (method.lower() == "post") and (header['Content-Type'] == 'application/json'):
                if 'setparam' in data:
                    if data['setparam'] is not None:
                        nn = GetParamBySequenceCall().get_params(data['setname'], data['setparam'])
                        global_vars.update(nn)
                else:
                    pass
                header, request_data = self.pre_request(header, pay_load)
                try:
                    logger.info(
                        "********************开始执行请求********************")
                    logger.info('请求头部为 ：{}'.format(header))
                    logger.info('请求方法为 ：{}'.format(method))
                    logger.info('请求路径为 ：{}'.format(url))
                    logger.info('请求数据为 ：{}'.format(request_data))
                    requests.packages.urllib3.disable_warnings()
                    rs = requests.post(url=url, data=json.dumps(request_data), headers=header, verify=False)
                    logger.info(f"接口请求成功,响应为：{rs.text}")
                except Exception as e:
                    logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{request_data}\n接口请求头：{header}\n"
                                 f"接口响应状态码：{rs.status_code}\n错误信息：{e}")
                resp = json.loads(rs.text)
                http_code = rs.status_code
                if data['extract'] is not None:
                    eval_jsonpath_str(json.loads(rs.text), data['extract'])
                self.respo.append(resp)
                self.respo.append(http_code)
            elif not header and (method.lower() == "post"):
                if 'setparam' in data:
                    if data['setparam'] is not None:
                        nn = GetParamBySequenceCall().get_params(data['setname'], data['setparam'])
                        global_vars.update(nn)
                else:
                    pass
                header, request_data = self.pre_request(header, pay_load)
                try:
                    logger.info(
                        "********************开始执行请求********************")
                    logger.info('请求头部为 ：{}'.format(header))
                    logger.info('请求方法为 ：{}'.format(method))
                    logger.info('请求路径为 ：{}'.format(url))
                    logger.info('请求数据为 ：{}'.format(request_data))
                    requests.packages.urllib3.disable_warnings()
                    rs = requests.post(url=url, data=request_data, headers={"ev": "v4"}, verify=False)
                    logger.info(f"接口请求成功,响应为：{rs.text}")
                except Exception as e:
                    logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{request_data}\n接口请求头：{header}\n"
                                 f"接口响应状态码：{rs.status_code}\n错误信息：{e}")
                resp = json.loads(rs.text)
                http_code = rs.status_code
                if data['extract'] is not None:
                    eval_jsonpath_str(json.loads(rs.text), data['extract'])
                self.respo.append(resp)
                self.respo.append(http_code)

            elif header and (method.lower() == "get"):
                if 'setparam' in data:
                    if data['setparam'] is not None:
                        nn = GetParamBySequenceCall().get_params(data['setname'], data['setparam'])
                        global_vars.update(nn)
                else:
                    pass
                header, request_data = self.pre_request(header, pay_load)
                try:
                    logger.info(
                        "********************开始执行请求********************")
                    logger.info('请求头部为 ：{}'.format(header))
                    logger.info('请求方法为 ：{}'.format(method))
                    logger.info('请求路径为 ：{}'.format(url))
                    logger.info('请求数据为 ：{}'.format(request_data))
                    requests.packages.urllib3.disable_warnings()
                    rs = requests.get(url=url, params=request_data, headers=header, verify=False)
                    logger.info(f"接口请求成功,响应为：{rs.text}")
                except Exception as e:
                    logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{request_data}\n接口请求头：{header}\n"
                                 f"接口响应状态码：{rs.status_code}\n错误信息：{e}")
                resp = json.loads(rs.text)
                http_code = rs.status_code
                if data['extract'] is not None:
                    eval_jsonpath_str(json.loads(rs.text), data['extract'])
                self.respo.append(resp)

                self.respo.append(http_code)
            # elif header and (method.lower() == "get") and (header['Content-Type'] == 'application/json'):
            #     header, request_data = self.pre_request(header, pay_load)
            #     try:
            #         logger.info(
            #             f"********************开始执行请求********************\t url:{url} \t pay_load:{request_data}")
            #         requests.packages.urllib3.disable_warnings()
            #         rs = requests.get(url=url, params=json.dumps(request_data), headers=header, verify=False)
            #         logger.info(f"接口请求成功,响应为：{rs.text}")
            #     except Exception as e:
            #         logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{request_data}\n接口请求头：{header}\n"
            #                      f"接口响应状态码：{rs.status_code}\n错误信息：{e}")
            #     resp = json.loads(rs.text)
            #     http_code = rs.status_code
            #     if data['extract'] is not None:
            #         eval_jsonpath_str(json.loads(rs.text), data['extract'])
            #     self.respo.append(resp)
            #     self.respo.append(http_code)
            elif not header and (method.lower() == "get"):
                if 'setparam' in data:
                    if data['setparam'] is not None:
                        nn = GetParamBySequenceCall().get_params(data['setname'], data['setparam'])
                        global_vars.update(nn)
                else:
                    pass
                header, request_data = self.pre_request(header, pay_load)
                try:
                    logger.info(
                        "********************开始执行请求********************")
                    logger.info('请求头部为 ：{}'.format(header))
                    logger.info('请求方法为 ：{}'.format(method))
                    logger.info('请求路径为 ：{}'.format(url))
                    logger.info('请求数据为 ：{}'.format(request_data))
                    requests.packages.urllib3.disable_warnings()
                    rs = requests.get(url=url, params=request_data, headers={"ev": "v4"}, verify=False)
                    logger.info(f"接口请求成功,响应为：{rs.text}")
                except Exception as e:
                    logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{request_data}\n接口请求头：{header}\n"
                                 f"接口响应状态码：{rs.status_code}\n错误信息：{e}")
                resp = json.loads(rs.text)
                http_code = rs.status_code
                if data['extract'] is not None:
                    eval_jsonpath_str(json.loads(rs.text), data['extract'])
                self.respo.append(resp)
                self.respo.append(http_code)

            # else:
            #     self.respo = {"code": False, "data": False}
            #     logger.info("没有找到对应的请求方法！")
            # logger.info("请求接口结果：\n {}".format(self.respo))

        return self.respo


if __name__ == '__main__':
    # test = ReqApi('/test_data/GetToken.yml', 'testcase1', 2)
    # test = ReqApi('/test_data/demo2.yaml', 'testcase1', 1, {'Token': '666'})
    # test1 = ReqApi('/test_case/Wakandahome/Login/test_agentEasyInfo.yml', 'testcase1', 1)
    # p = test1.run_request()
    # p1 = test.run_request()
    # print(p)
    test1 = ReqApi('/test_data/fosun_underwrite.yml', 'testcase1', 1)
    # test = ReqApi('/test_data/demo2.yaml', 'testcase1', 1, {'Token': '666'})
    # test2=ReqApi('/test_case/Wakandahome/Login/test_agentEasyInfo.yml', 'testcase1', 1)
    p1 = test1.run_request()
    # p2 = test2.run_request()
    print(p1)
