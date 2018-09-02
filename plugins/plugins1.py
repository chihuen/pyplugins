from plugins.Plugins import Plugins


class Plugins1(Plugins):
    def __init__(self):
        super(Plugins1, self).__init__()

    def handler_init(self):
        self.handler_register(self.func_1, "func1")
        self.handler_register(self.func_2, "func2")

    def func_1(self):
        print("%s func1 " % self.__class__.__name__)

    def func_2(self):
        print("%s func2 " % self.__class__.__name__)


def get_plugins_class():
    return Plugins1
