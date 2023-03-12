class Decorator:
    def add_handler(self, handler_dict, key):
        def decorator(handler):
            handler_dict[key] = handler
            return handler
        return decorator

    def hears(self, pattern):
        return self.add_handler(self.message_handlers, pattern)

    def commands(self, commands_list):
        for command in commands_list:
            self.add_handler(self.command_handlers, command)(handler_func)

    def command(self, command_str):
        return self.add_handler(self.command_handlers, command_str) 

    def callbacks(self, callbacks_list):
        def decorator(handler_func):
            for callback in callbacks_list:
                self.add_handler(self.callback_handlers, callback)(handler_func)
            def wrapper(*args, **kwargs):
                return handler_func(*args, **kwargs)
            return wrapper
        return decorator 

    def callback(self, callback_data):
        return self.add_handler(self.callback_handlers, callback_data)