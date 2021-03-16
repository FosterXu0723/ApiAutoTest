# 作者       ：yangwuxie
# 创建时间   ：2020/7/16 15:20
import json
import os
import sys
from typing import Any
import requests

from enum import Enum

from jsonpath import jsonpath

from common.Log import Log
from common.ReadConfig import ReadConfig
from utils.DingTalkRobot import errorCatch
from utils.ParamsUtils import is_params_need_handle, replace_params, global_vars, eval_jsonpath_str, parse_2_dict
from utils.YmlUtils import YamlRead
sys.path.append("..")

"""
接口请求函数
1.检查请求参数是否存在待替换的参数，有：替换
2.发送Http请求，拿到response
3.检查是否需求后置提取的参数，有：取出来
"""


logger = Log().get_logger()


@errorCatch
def do_request(file_name: str) -> Any:
    """
    读取yml文件发送http请求
    :param file_name: yml文件名称，完整的文件名称
    """
    file = os.path.join(ReadConfig().testDataDir, file_name)
    yml = YamlRead(file).yml
    # cases类型 list(dict1,dict2)
    cases = yml['testcase']
    for case in cases:
        case_name = case["name"]
        logger.debug(f"开始处理名称为：{case_name}的接口")
        requests_data = None
        url = None
        method = None
        headers = None
        data = None
        extract = None
        validate = None
        response = None
        try:
            requests_data = jsonpath(case, "$..requests")[0]
            logger.info(f"获取requests_data成功:{requests_data}")
        except Exception as e:
            logger.error(f"获取request_data失败，失败原因为：{e}")
        try:
            url = requests_data["url"]
            logger.info(f"获取url成功:{url}")
        except Exception as e:
            logger.error(f"获取url失败，失败原因为：{e}")
        try:
            method :str = requests_data["method"]
            logger.info(f"获取method成功:{method}")
            if method.upper() not in RequestMethodEnum.get_value():
                logger.warn(f"请求方式不合法：{method}")
        except Exception as e:
            logger.error(f"获取method失败，失败原因为：{e}")
        try:
            headers = requests_data["headers"]
            logger.info(f"获取headers成功:{headers}")
            if not headers:
                logger.warn("====请求头为空，即将采用默认请求头替换===")
        except Exception as e:
            logger.error(f"获取headers失败，失败原因为：{e}")
        try:
            data = requests_data["data"]
            logger.info(f"获取data成功:{data}")
        except Exception as e:
            logger.error(f"获取请求参数data失败，失败原因为：{e}")
        try:
            extract = requests_data['extract']
            logger.info(f"获取extract成功：{extract}")
        except Exception as e:
            logger.error(f"获取extract失败，失败原因为：{e}")
        try:
            validate = requests_data['validate']
            logger.info(f"获取validate成功：{validate}")
        except Exception as e:
            logger.error(f"获取validate失败，失败原因为：{e}")
        if not headers:
            headers = RequestHeaderEnum.NORMALHEADERS.value
            logger.warn(f"===采用默认请求头{headers}===")
        if is_params_need_handle(data):
            logger.info(f"接口请求体有需要处理的参数{data}")
            try:
                data = replace_params(data, global_vars)
                logger.info(f"处理请求参数成功，替换结束之后的参数为：{data}")
            except Exception as e:
                logger.error(f"参数处理失败,失败原因：{e}")
        try:
            response = requests.request(method=method, url=url, data=data, headers=headers, verify=False)
            logger.info(f"接口{case_name}请求成功,响应为：{response.text}")
        except Exception as e:
            logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{data}\n接口请求头：{headers}\n接口响应状态码："
                         f"{response.status_code}\n错误信息：{e}")
        if extract:
            logger.info(f"需要从响应体中提取参数：{extract}")
            try:
                eval_jsonpath_str(json.loads(response.text), extract)
                logger.info(f"参数提取成功，全局变量字典更新为：{global_vars}")
            except Exception as e:
                logger.error(f"参数提取失败，失败原因为：{e}")
        # todo
        if validate:
            pass


def http_request(url: str, method: str, headers: dict, pay_load: dict) -> requests.Response:
    """
    剥离跟业务的关联，仅专注于接口请求
    :param url: 请求地址
    :param method: 请求方式
    :param headers: 请求头
    :param pay_load: 请求参数
    :return:
    """
    if url and not url.startswith("http"):
        logger.warn(f"请求地址异常，建议格式 e.g: https://host/path,现url为：{url}")
    if method.upper() not in RequestMethodEnum.get_value():
        logger.warn(f"请求方式异常，请求方式为{method}")
    if not isinstance(headers, dict):
        logger.warn(f"传入headers:{headers}不是字典格式，将用默认headers替换")
        headers = RequestHeaderEnum.NORMALHEADERS.value
    if not isinstance(pay_load, dict):
        logger.warn(f"传入的pay_load:{pay_load}不是字典格式，尝试转为字典格式")
        try:
            pay_load = parse_2_dict(pay_load)
            logger.info(f"pay_load：{pay_load} 成功转为字典格式！！")
        except Exception as e:
            logger.error(f"pay_load：{pay_load} 转为字典失败，失败原因：{e}")
    response = None
    try:
        response = requests.request(method=method, url=url, data=pay_load, headers=headers, verify=False)
        logger.info(f"接口请求成功,响应为：{response.text}")
    except Exception as e:
        logger.error(f"接口请求失败，接口请求url：{url}\n接口请求参数：{pay_load}\n接口请求头：{headers}\n接口响应状态码："
                     f"{response.status_code}\n错误信息：{e}")
    return response


class RequestHeaderEnum(Enum):

    NORMALHEADERS = {"EV": "v4"}

    JSONTYPEHEADERS = {"EV": "v4", "content-type": "application/json"}

    URLTYPEHEADERS = {"EV": "v4", "content-type": "application/x-www-form-urlencoded"}


class RequestMethodEnum(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

    @staticmethod
    def get_value():
        return RequestMethodEnum.__dict__['_member_names_']


if __name__ == '__main__':
    do_request("test.yml")
