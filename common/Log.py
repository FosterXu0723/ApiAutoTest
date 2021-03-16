# -*- coding: utf-8 -*
# 作者       ：yangwuxie
# 创建时间   ：2020/6/3 14:41


import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from common.ReadConfig import ReadConfig


class Log(object):
    """
    通过实例化Log对象调用get_logger方法获取日志记录对象
    """

    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = ReadConfig()
        self.log_file_name = c.log_file_name if c and c.log_file_name else 'test.log'
        self.backup_count = c.log_limit if c and c.log_limit else 5
        self.console_output_level = c.log_console_level if c and c.log_console_level else 'DEBUG'
        self.file_output_level = c.log_file_output_level if c and c.log_file_output_level else 'DEBUG'
        pattern = c.log_pattern if c and c.log_pattern else '%(asctime)s - %(filename)s[line:%(lineno)d] - %(' \
                                                            'levelname)s: %(message)s'
        self.formatter = logging.Formatter(pattern)
        # 兼容mac os
        if sys.platform == 'darwin':
            self.log_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'log')
        else:
            self.log_path = os.path.join(os.path.split(os.path.dirname(__file__))[0].replace("/", "\\"), 'log')

    def get_logger(self):
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            file_handler = TimedRotatingFileHandler(filename=os.path.join(self.log_path, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=int(self.backup_count),
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Log().get_logger()

if __name__ == '__main__':
    # logger.info('error msg')
    pass
