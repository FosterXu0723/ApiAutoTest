# @time   :2020/08/03
# @author : YiCai
# coding: utf-8
import json

key_list = []


def get_dict_allkeys(dict_a):
    """
    遍历嵌套字典，获取json返回结果的所有key值
    :param dict_a:
    :return: key_list
    """

    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        # 如果为字典类型，则提取key存放到key_list中
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            key_list.append(temp_key)
            get_dict_allkeys(temp_value)  # 自我调用实现无限遍历
    elif isinstance(dict_a, list):
        # 如果为列表类型，则遍历列表里的元素，将字典类型的按照上面的方法提取key
        for k in dict_a:
            if isinstance(k, dict):
                for x in range(len(k)):
                    temp_key = list(k.keys())[x]
                    temp_value = k[temp_key]
                    key_list.append(temp_key)
                    get_dict_allkeys(temp_value)  # 自我调用实现无限遍历
    return key_list


if __name__ == "__main__":
    a={"code":10000,"msg":"Success","data":{"political":null,"nation":null,"education":null,"workArea":null,"bank":null,"pdfPath":[{"path":"https://contract-esign.oss-cn-hangzhou.aliyuncs.com/c835d2ea95a7486886b2a5411c049128","name":"《心有灵犀保险代理人协议》"}]},"success":true}
    b=json.loads(json.dumps(a))
    print(b)