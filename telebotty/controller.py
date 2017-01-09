from telegram.ext import CommandHandler, MessageHandler, Filters


class Controller(object):
    def __init__(self, app):
        self.app = app
        for attr_name in dir(self):
            function = getattr(self, attr_name)
            if hasattr(function, 'is_command'):
                command_query = getattr(function, 'query')
                self.app.handler.dispatcher.add_handler(CommandHandler(command_query, function))

            elif hasattr(function, 'is_inline'):
                regex_query = getattr(function, 'query')
                self.app.handler.add_inline_handler(regex_query, function)

            elif hasattr(function, 'is_message'):
                filters = [Filters.text]
                if hasattr(function, 'filters'):
                    filters += function.filters
                print('Message handler:', function, filters)

                def all_filters(msg):
                    return all([filter_func(msg) for filter_func in filters])

                self.app.handler.dispatcher.add_handler(
                    MessageHandler([all_filters], function))


def command(query):
    def decorator(func):
        func.is_command = True
        func.query = query
        return func

    return decorator


def message():
    def decorator(func):
        func.is_message = True
        return func

    return decorator


def filter_message(filter_func):
    def decorator(func):
        if not hasattr(func, 'filters'):
            func.filters = []
        func.filters.append(filter_func)
        return func

    return decorator


def inline(query_regex):
    def decorator(func):
        func.is_inline = True
        func.query = query_regex
        return func

    return decorator
