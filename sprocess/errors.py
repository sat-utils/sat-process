
class BaseException(Exception):
    default_msg = None

    def __init__(self, msg=None):
        msg = msg if msg else self.default_msg
        Exception.__init__(self, msg)


class SatProcessError(Exception):
    pass


class SceneIsNotOpen(BaseException):
    default_msg = 'Scene is not opened. Open it first'


class AssignBandNames(BaseException):
    default_msg = 'You have to assign band names to each file first'
