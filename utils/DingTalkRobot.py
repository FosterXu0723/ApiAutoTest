# 作者       ：yangwuxie
# 创建时间   ：2020/7/17 16:35
import functools
import sys
import traceback
import requests
import json


def errorCatch(func):
    """
    抓取错误日志发送到钉钉群
    :param func:
    :return:
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            json_data = {
                "msgtype": "text",
                "title": sys._getframe().f_code.co_filename,
                "text": {"content": "方法名：" + func.__name__ + "\n" + traceback.format_exc()},
                "at": {
                    "atMobiles": [17602116237]
                }
            }
            requests.post(url="https://oapi.dingtalk.com/robot/send?access_token=69b4e53009f7f36c0216a0df6fd8c5c85af0a77bb2201968da5d4da0d298e04c",
                          data=json.dumps(json_data),headers={"content-type":"application/json"},verify=False)
    return inner


def remindFailure():
    json_data = {
        "msgtype": "text",
        "text": {
            "content": "Error: 自动化case未通过，请及时维护"
        },
        "at": {
            "atMobiles": [
                '17602116237',
                '13175020347',
                '18758168675',
                '15157543598'
            ],
            "isAtAll": False
        }
    }
    requests.post(
        url="https://oapi.dingtalk.com/robot/send?access_token=69b4e53009f7f36c0216a0df6fd8c5c85af0a77bb2201968da5d4da0d298e04c",
        data=json.dumps(json_data), headers={"content-type": "application/json"}, verify=False)


if __name__ == '__main__':
    remindFailure()


