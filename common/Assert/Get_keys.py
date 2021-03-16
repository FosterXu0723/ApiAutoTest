# @time   :2020/08/12
# @author : YiCai
# coding: utf-8
"""
获取字典中最外层value值不为None的keys,不适用嵌套的字典
"""


def get_keys(dict_a):
    key_list = []
    for k, v in dict_a.items():
        if v is not None:
            key_list.append(k)
    return key_list


if __name__ == '__main__':
    a = {'expected_code': None, 'assert_in_text': 'Succes', 'assert_key_exists': 'success'}
    print(get_keys(a))
