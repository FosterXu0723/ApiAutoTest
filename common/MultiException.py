# 作者       ：yangwuxie
# 创建时间   ：2020/7/14 17:04


class SplitException(Exception):
    def __init__(self, error="截断出现错误"):
        super().__init__(self, error)


class NodeNotFoundException(Exception):
    def __init__(self, error="找不到指定的节点"):
        super().__init__(self, error)


class SheetTypeError(Exception):
    def __init__(self, error="表类型错误"):
        super().__init__(self, error)


class YamlKeyError(BaseException):
    def __init__(self, error="文件中找不到对应的key"):
        super().__init__(self, error)