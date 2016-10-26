from telegram.ext import CommandHandler


class Controller(object):
    def __init__(self, app):
        self.app = app
        for attr_name in dir(self):
            function = getattr(self, attr_name)
            if hasattr(function, 'is_command'):
                command_query = getattr(function, 'query')
                self.app.updater.dispatcher.add_handler(CommandHandler(command_query, function))

            elif hasattr(function, 'is_inline'):
                regex_query = getattr(function, 'query')
                self.app.add_inline_handler(regex_query, function)


def command(query):
    def decorator(func):
        func.is_command = True
        func.query = query
        return func

    return decorator


def inline(query_regex):
    def decorator(func):
        func.is_inline = True
        func.query = query_regex
        return func

    return decorator
