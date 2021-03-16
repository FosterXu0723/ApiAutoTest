# @time   :2020/08/02
# @author : YiCai


def get_target_value(key, dic, tmp_list):
    """
    获取目标key的value值
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '
    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    for value in dic.values():  # 传入数据不符合则对其value值进行遍历
        if isinstance(value, dict):
            get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
        elif isinstance(value, (list, tuple)):
            _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list


def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)  # 传入数据的value值是列表或者元组，则调用自身


if __name__ == '__main__':
    test_dic = {'a': '1', 'b': '2',
                'c': {
                    'd': [{'e': [{'f': [{'v': [{'g': '6'}, [{'g': '7'}, [{'g': 8}]]]}, 'm']}]}, 'h', {'g': [10, 12]}]}}
    l = [{'casename': '登录成功', 'caseno': 'testcase1', 'step': 2}, {'casename': '登录失败', 'caseno': 'testcase2', 'step': 1}]
    ll = ''
    for i in l:
        ll = ll+(''.join(get_target_value('caseno', i, [])))
    print(ll)
