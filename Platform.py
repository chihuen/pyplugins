# -*- encoding: utf-8 -*-
import os
import sys
import importlib.util
import importlib
from plugins.Plugins import Plugins


class Platform(Plugins):
    __ROOT__ = os.path.dirname(os.path.realpath(__file__)) + '/plugins'

    def __init__(self):
        super(Platform, self).__init__()
        self.plugins = {}
        self.load_plugins()
        print(self.plugins)

    def is_plugins_exist(self, target):
        return True if target in self.plugins.keys() else False

    def load_plugins(self, path=None):
        if not path:
            path = Platform.__ROOT__

        if not os.path.isdir(path):
            raise ValueError("{0} is not a valid directory".format(path))

        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            if os.path.isdir(file_path):
                self.load_plugins(file_path)
            else:
                if file.startswith('_') or not file.endswith('.py'):
                    continue

                module_name = os.path.splitext(file)[0]

                # 暂时不允许覆盖已导入的模块，如果以后有打补丁需求再修改
                if module_name in sys.modules:
                    exist_mod_spec = importlib.util.find_spec(module_name)
                    print(
                        "module '{0}' in \"{1}\" will not be loaded:\n  Same name module in \"{2}\" has been loaded".format(module_name,
                                                                                                            file_path,
                                                                                                            exist_mod_spec.origin))
                    continue
                else:
                    # 进行了上面的文件筛选以及file_path路径正确，以下两行一般不会出现问题,否则spec为None
                    spec = importlib.util.spec_from_file_location(module_name, file_path)  # 创建ModuleSpec对象
                    module = importlib.util.module_from_spec(spec)  # 创建模块对象
                    spec.loader.exec_module(module)  # 初始化模块对象
                    sys.modules[module_name] = module

                try:
                    # 插件必须有get_plugins_class方法
                    clazz = module.get_plugins_class()
                    # 插件类必须继承Plugins类
                    if not issubclass(clazz, Plugins):
                        continue

                    self.plugins[str(clazz.__name__)] = {}
                    self.plugins[str(clazz.__name__)]['object'] = clazz()
                    self.plugins[str(clazz.__name__)]['path'] = file_path

                    # 插件类必须继承Plugins类
                    self.plugins[str(clazz.__name__)]['object'].handler_init()

                except AttributeError:
                    continue

    def find_handler_in_plugins(self, method):
        for target in self.plugins.keys():
            clazz = self.plugins[target]['object']
            if not clazz.is_handler_exist(method):
                continue
            else:
                return clazz.handler_finder(method)
        raise ValueError("Can not find this handler in {plugins}!: {method}".format(plugins=self._target, method=method))

    def find_handler(self, method, target=None):
        # 遍历所有
        if not target:
            try:
                return self.handler_finder(method)
            except ValueError:
                return self.find_handler_in_plugins(method)

        # 遍历Platform
        if target == self._target:
            return self.handler_finder(method)

        # 遍历plugins
        if not self.is_plugins_exist(target):
            raise ValueError("Platform {platform} has no plugins \"{plugins}\"".format(platform=self._target, plugins=target))
        else:
            return self.plugins[target]['object'].handler_finder(method)

    @property
    def all_handlers(self):
        methods = []
        methods.extend(self.handlers)
        for plugins in self.plugins.keys():
            methods.extend(self.plugins[plugins]['object'].handlers)
        return methods


if __name__ == "__main__":
    platform = Platform()
    print(platform.handlers)
    print(platform.all_handlers)
    handler = platform.find_handler(method='func1')
    print(handler)
