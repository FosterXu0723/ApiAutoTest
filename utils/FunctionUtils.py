# 作者       ：yangwuxie
# 创建时间   ：2020/8/7 14:17

"""
处理数据文件中的function,统一采用 $function_name()
注意：数据文件中的方法必须要在DataRandomUtils文件中声明
"""
import importlib
import re
import sys
sys.path.append("..")
from typing import Any, List
from common.Log import logger
from utils.DataRandomUtils import get_function_dict, get_function_mapping
from utils.DingTalkRobot import errorCatch


def process_function(content: Any) -> Any:
    """
    {"test": $generate_date(1,2)} 处理data参数中的function
    :param content:
    :return:
    """
    pattern = r'\$\w+.*?\)'
    if isinstance(content, (list, tuple, dict)):
        content = str(content)
        args_list = get_function_args(content)
        match_list = re.findall(pattern, content)
        # 获取方法名称和内存地址
        function_dict = get_function_dict()
        for index, match in enumerate(match_list):
            for func_name in function_dict.keys():
                if match.__contains__(func_name):
                    if args_list[index]:
                        # 执行方法
                        function_result = function_dict[func_name](*args_list[index])
                    else:
                        # 没有参数直接执行
                        function_result = function_dict[func_name]()
                    if not isinstance(function_result, str):
                        function_result = str(function_result)
                    content = re.sub(pattern, function_result, content, 1)
        return eval(content)
    elif isinstance(content, str):
        args_list = get_function_args(content)
        match_list = re.findall(pattern, content)
        # 获取方法名称和内存地址
        function_dict = get_function_dict()
        for index, match in enumerate(match_list):
            for func_name in function_dict.keys():
                if match.__contains__(func_name):
                    # 执行方法
                    if args_list:
                        # 执行方法
                        function_result = function_dict[func_name](*args_list[index])
                    else:
                        # 没有参数直接执行
                        function_result = function_dict[func_name]()
                    if not isinstance(function_result, str):
                        function_result = str(function_result)
                    content = re.sub(pattern, function_result, content, 1)
        return content


@errorCatch
def get_function_args(content: Any) -> List[List]:
    """
    获取方法参数
    :param content:
    :return:
    """
    pattern = r'\$.*?\)'
    result = list()
    if not isinstance(content, str):
        content = str(content)
    match_list = re.findall(pattern, content)
    # 没有匹配上直接返回
    if not match_list:
        return None
    for match in match_list:
        start_index = str(match).index("(") + 1
        end_index = match.index(")")
        try:
            args = match[start_index:end_index]
            # 没有参数
            if not args:
                # 写入空list
                result.append(list())
                continue
            split = args.split(",")
            # result.append(list(map(lambda x: int(x.strip()), split)))
            args_list = []
            for argument in split:
                try:
                    args_list.append(int(argument))
                except Exception as e:
                    args_list.append(str(argument))
            result.append(args_list)
            # todo 字典类型
        except Exception as e:
            logger.error(e)
    return result


def is_args_contains_function(content: Any):
    """
    返回判断
    :param content:
    :return:
    """
    if not isinstance(content, str):
        content = str(content)
    return True if re.search(r'\$.*?\)', content) else False


def process_multy_function(raw_string: str):
    """
    实现方法参数引用另外一个方法返回值
    >>>process_multy_function("$fuson_order_new($fosun_orderno())")
    426172351413313
    :return 方法执行过后的原始字符串
    """
    try:
        args_start_index = raw_string.index("(", 0)
        args_end_index = raw_string.index(")", -1)
        args_content = raw_string[args_start_index + 1:args_end_index]
        # $func_name(args), 55
        argument_list = [arg.strip(" ") for arg in args_content.split(",")]
        for argument in argument_list:
            if is_args_contains_function(argument):
                # 返回执行结果
                function_result = process_function(argument)
                # 执行结果加入原始函数的参数中
                args_content = args_content.replace(argument, function_result)
        # 执行完成之后的参数放入外层的函数体中
        raw_string = raw_string[0:args_start_index + 1] + args_content + raw_string[args_end_index:]
        return process_function(raw_string)
    except Exception:
        return raw_string



if __name__ == '__main__':
    print(process_multy_function("$fuson_order_new($fosun_orderno())"))





