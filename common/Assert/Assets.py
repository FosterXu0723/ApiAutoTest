# @time   :2020/07/30 0820
# @author : YiCai
import json
import os
from common.Assert.readYmal_validata import read_yaml_val
from common.Log import logger
from common.Assert.Get_Target_Value import get_target_value
from common.Assert.Get_All_Keys import get_dict_allkeys
from common.Assert.Get_keys import get_keys

import sys
import os

sys.path.append("..")
# sys.path.append('../')

sys.setrecursionlimit(5000)


class Assert:
    def __init__(self, test_names, test_steps_no, code, response_data, case_path):
        """
        :parameter test_steps 单步测试用例 step1中的1
        :parameter code http 状态码
        :parameter response_data 接口返回值
        :parameter case_path 接口路径
        """

        self.code = code
        self.response_data = response_data
        self.validate = read_yaml_val(test_names, test_steps_no, case_path)

    def check_code(self):
        if self.validate['expected_code'] is not None:
            # print(type(self.validate['expected_code']))
            # print(type(self.code))
            assert self.code == (self.validate['expected_code']), "expected_code 断言-----http状态码错误！ {0} != {1}".format(
                self.code, self.validate["expected_code"])
        else:

            # logger.info('此step下的validate节点下的 {} 类型节点的值为空，无需断言'.format('expected_code'))
            print('此step下的validate节点下的 {} 类型节点的值为空，无需断言'.format('expected_code'))

    def check_keys_value(self):
        if self.validate['assert_kes_value'] is not None:
            # print(type(self.validate['assert_kes_value']))
            val_list = self.validate['assert_kes_value']
            # print('jjjj {}'.format(val_list))

            for i in val_list:
                # print('xxx种的类型为 {}'.format(type(i)))
                obj_key = list(i.keys())[0]
                logger.info('要断言的key为 {}'.format(obj_key))
                obj_value = list(i.values())[0]
                logger.info('要断言的key的value值为 {}'.format(obj_value))
                temp = self.response_data
                # print(type(temp))
                # logger.info('接口返回的结果【用来断言】为 {}'.format(temp))
                keys_value = get_target_value(obj_key, temp, [])
                # print(keys_value)
                assert obj_value in keys_value, (
                    'assert_kes_value 断言-----接口中字段 {} 的值 {} 和预期结果的值 {} 不一致'.format(obj_key, keys_value, obj_value))
        else:
            pass

    def check_in_text(self):
        if self.validate['assert_in_text'] is not None:
            # logger.info('接口返回的结果【用来断言】为 {}'.format(self.response_data))
            text = (self.validate['assert_in_text']).split(',')
            res_ = json.dumps(self.response_data, ensure_ascii=False)#.replace('": ', '":')
            # print(text)
            print(res_)
            for i in text:
                assert str(i) in res_, 'assert_in_text 断言-----接口的返回数据中不包含期望值 {} '.format(i)

    def check_key(self):
        """
        预期结果='key1,key2,ke3....'
        实际结果='{"key1":"123456","key2":"1111"}'
        :return:
        """
        if self.validate['assert_key_exists'] is not None:
            # logger.info('接口返回的结果【用来断言】为 {}'.format(self.response_data))
            check_data = self.validate['assert_key_exists']
            check_data_list = check_data.split(',')
            # print(check_data_list)
            # res_list = []  # 存放每次比较的结果
            # wrong_key = []  # 存放比较失败key
            # print(type(self.response_data))
            res_data = get_dict_allkeys(json.loads(json.dumps(self.response_data)))
            logger.info('所有的key为 {}'.format(res_data))

            for i in check_data_list:
                assert i in res_data, 'assert_key_exists 断言-----预期结果的中的key {} 不在接口的返回结果中的key {} 集合中'.format(
                    i, res_data)
        else:
            pass

    def check_result(self):
        logger.info('接口返回的结果【用来断言】为 {}'.format(self.response_data))
        print('断言的集合为  {}'.format(self.validate))
        print('接口返回的结果【用来断言】为 {}'.format(self.response_data))
        logger.info('yml种预期的validate is {}'.format(self.validate))
        if self.validate is not None:

            val_keys = get_keys(self.validate)
            logger.info('要断言的validate类型列表为 {}'.format(val_keys))
            try:
                for i in val_keys:
                    if i == 'expected_code':
                        # if self.validate['expected_code'] is not None:
                        self.check_code()
                    # else:
                    #     print('此step下的validate节点下的 {} 类型节点的值为空，无需断言'.format('expected_code'))

                    elif i == 'assert_kes_value':
                        self.check_keys_value()

                    elif i == 'assert_in_text':
                        self.check_in_text()
                    elif i == 'assert_key_exists':
                        self.check_key()
                logger.info('此step中的validate "断言成功')
            except:
                logger.error('此step中的validate "断言失败" ')
                assert False, '此step中的validate "断言失败" '

            # except Exception as e:
            #     # logger.error(e)
            #     assert False, logger.error('此step中的validate "断言失败" ')
        else:
            logger.warning('此step中的validate为 {}所以没有要断言的内容'.format(self.validate))
            assert True, '没有要断言的内容'


if __name__ == '__main__':
    # # baseDir = os.path.split(os.path.dirname(__file__))[0]
    # baseDir = '../../'
    # testDataDir = os.path.join(baseDir, "test_data")  # 这里用join 在win10下会有双斜杠的问题
    # case = os.path.join(testDataDir, "test_agentEasyInfo.yml")

    case = '/test_data/test_agentEasyInfo.yml'
    case = case.replace('\\', '/')
    res = {'code': 10000, 'data': 'Succes'}
    print(case)
    a = Assert('testcase1', 1, 200, res, case)
    a.check_code()
