# 作者       ：yangwuxie
# 创建时间   ：2020/7/28 9:53
import os
import sys
import yaml
from ruamel import yaml
sys.path.append("..")
from common.Log import Log
from common.ReadConfig import ReadConfig


class YamlRead(object):

    def __init__(self, path: str):
        self.path = path
        self.log = Log().get_logger()
        if not os.path.exists(self.path):
            self.log.error(f"指定文件路径不存在：{self.path}")
        self.yml = None
        with open(path, 'r', encoding='utf-8') as f:
            try:
                self.yml = yaml.safe_load(f.read())
            except Exception as e:
                print(e)

    def get_cases(self):
        try:
            cases = self.yml['testcase']
            return cases
        except KeyError:
            self.log.error(f"从文件： {self.path} 获取testcase失败")


def create_yml_template(filename: str):
    """
    生成yml文件模板
    :param filename: 文件名
    :return: 文件
    """
    test_data_dir = os.path.join(ReadConfig.proDir, "test_data")
    file_path = os.path.join(test_data_dir, filename)
    if os.path.exists(file_path):
        return None
    template_dict = {'testcase1':
                         {'casename': "value",
                          'Enabled': "value",
                          'step1':
                              {'name': "value",
                               'general':
                                   {'path': "value",
                                    'method': "value"},
                               'headers':
                                   {'Content-Type': "value",
                                    'Ev': "v4", },
                               'data':
                                   {'key': "value"},
                               'extract':
                                   {'key': '$..key'},
                               'validate':
                                   {"expected_code": "status_code",
                                    "assert_kes_value": [{"code": 10000}],
                                    "assert_in_text":'Succes,"code":10000',
                                    "assert_key_exists":'data,functionPermissionList'}
                               },
                          'headersparamsvalue': {},
                          'dataparamsvalue': {}
                          }
                     }
    with open(file_path, 'w', encoding="utf-8") as f:
        yaml.dump(template_dict, f, Dumper=yaml.RoundTripDumper)


if __name__ == '__main__':
    create_yml_template("sensitiveWordConfiguration.yml")
