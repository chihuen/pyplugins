class Plugins:
    def __init__(self):
        self._target = self.__class__.__name__
        self._handlers = {}

    def is_handler_exist(self, method):
        return True if method in self._handlers.keys() else False

    def handler_register(self, handler, method):
        if not self.is_handler_exist(method):
            self._handlers[method] = {}

        self._handlers[method]['handler'] = handler
        print("Plugins \"%s\" register handler %s" % (self._target, self._handlers[method]['handler']))

    def handler_init(self):
        pass

    def handler_finder(self, method):
        try:
            handler = self._handlers[method]['handler']
        except Exception:
            raise ValueError("Can not find this handler \"{method}\" in \"{plugins}\"".format(plugins=self._target, method=method))
        else:
            return handler

    def execute(self, method, data):
        return self.handler_finder(method)(data)

    @property
    def handlers(self):
        return [method for method in self._handlers.keys()]