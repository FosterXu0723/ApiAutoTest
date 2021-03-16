#  date:  2020/9/11
#  Author:  jinmu
#  Description:  获取另外yml文件里面要替换的参数

import sys
sys.path.append("../..")
from common.handle_yaml import *
from common import ReqApi
from utils import ParamsUtils
from common.Log import Log


class GetParamBySequenceCall:

    def get_params(self,casename,targetparam):
        getdata = HandleYaml(casename).get_casename_step()  # 获取到用例所需数据
        print('getdata的值是：{}'.format(getdata))
        try:
            for item in getdata:
                caseno=item['caseno']
                step=item['step']
                api = ReqApi.ReqApi(casename, caseno, step)#初始化请求的类
                res = api.run_request()
                res_1=ParamsUtils.eval_jsonpath_str(res,targetparam)
                logger.info('获取到之前yml需要替换数据：{}'.format(res_1))
                return res_1
        except  Exception as e:
            logger.error('获取之前yml需要替换数据失败{}'.format(e))

if __name__ == '__main__':
    targetparam={'tradeKey': '$..tradeKey'}
    res=GetParamBySequenceCall().get_params('/test_data/submit.yml',targetparam)
    print('res的值是:{}'.format(res))



