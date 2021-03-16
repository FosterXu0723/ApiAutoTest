#coding=utf-8
# 作者       ：yangwuxie
# 创建时间   ：2020/7/14 17:01
"""
处理Excel读取出来的参数
"""
import ast
import json
import re
import sys
sys.path.append("..")
from json import JSONDecodeError
from typing import Dict, Any, Text
from jsonpath import jsonpath
from common.Log import Log
from common.MultiException import SplitException
from utils.DingTalkRobot import errorCatch

logger = Log().get_logger()

global_vars: Dict[Any, Any] = dict()


@errorCatch
def parse_2_dict(source: str):
    """
    把参数处理成数组
    :param source: key:value,key:value
    :return: result_dict
    """
    # 表示只存在一对键值对
    if not source.__contains__(","):
        _list = source.split(":")
        return {_list[0]: _list[1]}
    try:
        key_value_source = source.split(",")
        result_dict = {}
        for i in key_value_source:
            key_value = i.split(":")
            if len(key_value) != 2:
                logger.error("源数据不符合键值对规范，请检查数据")
                return
            result_dict[key_value[0].strip("\"")] = key_value[1].strip("\"")
        return result_dict
    except Exception as e:
        logger.error(SplitException("源数据分隔失败，请检查源数据:{}".format(source)))


@errorCatch
def replace_params(source_dict: dict, dest: dict):
    """
    处理替换参数,需要满足key:value的形式
    source  {test:${todo_id},test2:${todo2_id}}
    :param dest: 替换内容 {"test": 123}
    :param source_dict: 待替换字符 {test: ${test}}
    :return: 替换完成之后的dict
    """
    pattern = r'\$\{.*?\}'
    json_str = str(source_dict)
    match_list = re.findall(pattern, json_str)
    if len(match_list) == 0:
        logger.warning("目标源没有参数需要处理，source_dict：{}".format(source_dict))
        return eval(json_str)
    # if len(match_list) != len(dest.keys()):
    #     logger.warning("目标参数过多，请检查，dest：{}".format(dest))
    #     return eval(json_str)  # 直接返回，节省资源
    for match in match_list:
        is_change = False
        for key in dest.keys():
            if is_change:
                break
            dest_str_value = ""
            # 是否包含key
            if not match.__contains__(key):
                continue
            # 判断是否为str，re.sub中需要参数str
            if not isinstance(dest[key], str):
                dest_str_value = str(dest[key])
            else:
                dest_str_value = dest[key]
            json_str = re.sub(pattern, dest_str_value, json_str, 1)
            is_change = True
    return eval(json_str)


@errorCatch
def eval_jsonpath_str(source_dict: dict, jsonpath_dict: dict):
    """
    执行jsonpath,提取yml中设置的待提取的字段
    :param jsonpath_dict:  jsonpath提取数据表达式  {token: $..token,test: $..ttt}
    :param source_dict: 全局源数据字典，jsonpath从source_dict中查找匹配数据
    :return: 执行结果
    """
    if not jsonpath_dict:
        logger.info("没有需要提取的参数")
        return
    try:
        result = {}
        try:
            for key, value in jsonpath_dict.items():
                # 返回匹配结果
                matct_case = jsonpath(source_dict, value)
                if matct_case:
                    logger.info(f"从源:{source_dict} 中成功提取{value}")
                else:
                    logger.info(f"从源:{source_dict} 中成功提取{value}")
                    continue  # 表示match_case为False
                # 默认用第一个
                result[key] = matct_case[0]
        except Exception as e:
            logger.error(f"源数据{source_dict}中找不到{value}，请检查")
        # 更新全局变量字典
        global_vars.update(result)
        logger.info(f"参数处理完成，结果为{result}")
        return result
    except Exception as e:
        logger.error("入参格式错误，请检查：{}".format(jsonpath_dict))


@errorCatch
def is_params_need_handle(source: dict) -> bool:
    """
    判断是否需要处理
    :param source:待处理源数据
    :return:返回布尔类型
    """
    return True if re.search(r'\$\{.*?\}', str(source)) else False


@errorCatch
def extract_data(source: dict, node: str) -> list:
    """
    从response中拿到内容
    :param source:
    :param node:
    :return:匹配结果集
    """
    if not isinstance(source, dict):
        logger.error("入参不是字典类型，实例化jsonpath出错")
    if not isinstance(node, str) and not node.startswith("$"):
        logger.error('检索表达式格式错误，请检查：{}'.format(node))
    return jsonpath(source, node)


def read_param(test_name, param, _path, relevance=None):
    '''
    读取用例中的请求参数 parameter
    :param _path:
    :param test_name: 用例名称
    :param param: parameter或参数的文件名称

    :param relevance:
    :return:
    '''
    if isinstance(param, dict):
        param = replace(param, relevance)
    elif isinstance(param, list):
        param = replace(param, relevance)
    elif param is None:
        pass
    else:
        try:
            # 当请求参数引用的是文件时
            with open(_path + '/' + param, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i in data:
                    if i["test_name"] == test_name:
                        param = i['parameter']
                        break
                    if not isinstance(param, dict):
                        raise Exception("未能找到用例关联的参数\n文件路径：%s\n索引：%s" % (param, _path))
                    else:
                        param = replace(param, relevance)
        except FileNotFoundError:
            raise Exception("用例关联文件不存在\n文件路径： %s" % param)
        except JSONDecodeError:
            raise Exception("用例关联的参数文件有误\n文件路径： %s" % param)
    return param


def replace(param, relevance=None):
    """
    替换关联数据
    :param param: 请求参数
    :param relevance: 关联对象
    :return:
    """
    if isinstance(param, dict):
        for key, value in param.items():
            if isinstance(value, dict):
                param[key] = replace(value, relevance)
            elif isinstance(value, list):
                for k, i in enumerate(value):
                    param[key][k] = replace(i, relevance)
            else:
                try:
                    relevance_list = re.findall(r"\${(.*?)}\$", value)

                    relevance_index = 0
                    for n in relevance_list:
                        pattern = re.compile(r'\${' + n + r'}\$')
                        n = n.lower()
                        try:
                            if isinstance(relevance[n], list):
                                try:
                                    param[key] = re.sub(pattern, relevance[n][relevance_index], param[key], count=1)
                                    relevance_index += 1
                                except IndexError:
                                    relevance_index = 0
                                    param[key] = re.sub(pattern, relevance[n][relevance_index], param[key], count=1)
                                    relevance_index += 1
                            else:
                                param[key] = re.sub(pattern, relevance[n], param[key], count=1)
                        except KeyError:
                            pass
                except TypeError:
                    pass
                try:
                    param[key] = param[key]
                except TypeError:
                    pass

    elif isinstance(param, list):
        for k, i in enumerate(param):
            param[k] = replace(i, relevance)
    else:
        try:
            relevance_list = re.findall(r"\${(.*?)}\$", param)
            relevance_index = 0
            for n in relevance_list:
                pattern = re.compile(r'\${' + n + r'}\$')
                try:
                    if isinstance(relevance[n], list):
                        try:
                            param = re.sub(pattern, relevance[n][relevance_index], param, count=1)
                            relevance_index += 1
                        except IndexError:
                            relevance_index = 0
                            param = re.sub(pattern, relevance[n][relevance_index], param, count=1)
                            relevance_index += 1
                    else:
                        param = re.sub(pattern, relevance[n], param)
                except KeyError:
                    pass
        except TypeError:
            pass

    return param


def parse_string_value(str_value: Text):
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        return str_value


if __name__ == '__main__':
    #a={'asyn':'0','batchNo':'${batchNo}', 'body': '{"additionCoverages":[],"agentInfo":{"agentCode":"W20190708002","agentName":"朱卫杰","certificateNo":"21009000000080002019000232","gender":"1","identityCode":"21312313232312347","identityType":"1","mobile":"13770703079"},"applyTime":"${applyTime}","bankInfo":{"accountName":"接口数据","bankAccountNo":"6226096555840043","bankCode":"icbc","bankName":"工商银行"},"beneficiaries":[],"companyName":"复星联合","effectiveDate":"${effectiveDate}","enquiryPremium":"1560.00","goodsCode":"WZXFXBG00101","insuredInfos":[{"age":30,"birthday":"1990-01-02","contactAddressInfo":{"address":"西溪银座E座4楼","areaCode":"330106","areaName":"西湖区","cityCode":"330100","cityName":"杭州市","provinceCode":"330000","provinceName":"浙江省"},"email":"444@qq.com","gender":"1","height":"170","identityCode":"440115199001025959","identityExpirationDate":"2023-01-01","identityLongTermEffective":"0","identityType":"1","index":1,"isLegalBeneficiary":"1","jobCateDesc":"机关团体内勤人员","jobCateId":"000101","jobCateLevel":1,"mobile":"17035551263","name":"接口数据","relationWithProposer":"1","taxPayerType":"1","weight":"60"}],"mainCoverages":[{"amount":"100000.00","coveragePeriod":"0","coverageType":"L","insurePlan":"PLAN1","insuredIds":["1"],"payPeriod":"30","payPeriodType":"Y","premiumInsure":"1560.00","productName":"倍吉星重大疾病保险","salesCode":"WZXFXBM00101"}],"orderNo":"${orderNo}","proposerInfo":{"age":30,"birthday":"1990-01-02","contactAddressInfo":{"address":"西溪银座E座4楼","areaCode":"330106","areaName":"西湖区","cityCode":"330100","cityName":"杭州市","provinceCode":"330000","provinceName":"浙江省"},"email":"444@qq.com","gender":"1","identityCode":"440115199001025959","identityExpirationDate":"2023-01-01","identityLongTermEffective":"0","identityType":"1","index":0,"mobile":"17035551263","name":"接口数据","taxPayerType":"1"},"upperBankInfo":{"accountName":"接口数据","bankAccountNo":"6226096555840043","bankCode":"icbc","bankName":"工商银行"}}', 'companyCode': 'fosun', 'orderNo': '${orderNo}', 'type': 'insure'}
    #a={'asyn':'0','batchNo':'${batchNo}','batchNo':'${batchNo}'}
    #b={'batchNo':'test5020d31e0aa60b484644','applyTime':'2020-08-20 11:32:01','effectiveDate':'2020-08-21 00:00:00','orderNo':'test426172351457810'}
    #print (replace_params(a,b))
    #print(parse_string_value("22"))
    #a={'code': 10000, 'msg': 'Success', 'data': {'count': 1, 'data': [{'id': 19, 'formName': '接口自动化测试表单', 'formType': 1, 'formCode': 'JKZDHBD', 'creator': 'admin', 'updateTime': '2020-09-08 17:14:04', 'status': 0, 'statusStr': '待发布'}]}, 'success': True}
    #a={'asyn':'0','batchNo':'${batchNo}','batchNo':'${batchNo}'}
    #b={code: $..code}
    #print(eval_jsonpath_str(a, b))
    w={'a':'${n}','b':"123",'c':'${m}'}
    v={'n':"55","m":"66"}
    print (replace_params(w,v))

    

    

