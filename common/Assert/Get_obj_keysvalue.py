# @time   :2020/08/03
# @author : YiCai
# coding: utf-8
import types

'''
key有重复时不可用
'''
# 获取字典中的objkey对应的值，适用于字典嵌套
# dicts:字典
# objkey:目标key
# default:找不到时返回的默认值
def dict_get(dicts, objkey, default):
    tmp = dicts
    for k, v in tmp.items():
        if k == objkey:
            return v
        else:
            if isinstance(v, dict):
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default


# 如
dicttest = {'a': '1', 'b': '2',
            'c': {
                'd': [{'e': [{'f': [{'v': [{'g': '6'}, [{'g': '7'}, [{'g': 8}]]]}, 'm']}]}, 'h', {'g': [10, 12]}]}}
ret = dict_get(dicttest, 'g', None)
print(ret)
