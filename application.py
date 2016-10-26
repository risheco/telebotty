import logging
import os
import inspect
import glob
import importlib
import re
import sys
from os.path import join

from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler, MessageHandler, ChosenInlineResultHandler


def get_classes(package):
    classes = []
    for file in glob.glob(join(os.path.dirname(sys.argv[0]), package, "*.py")):
        name = os.path.splitext(os.path.basename(file))[0]
        module = importlib.import_module('%s.%s' % (package, name))

        classes += [cl for name, cl in inspect.getmembers(module, inspect.isclass)]

    return classes


class Application(object):
    def __init__(self, token):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(InlineQueryHandler(self.inline_query_dispatcher))

        self.inline_query = []
        self.inject_dependencies()

        #
        def callback_query_handler(bot, update):
            logging.log(logging.WARNING, "Unimplemented event callback_query_handler:")
            print("\t" + str(update))

        def message_handler(bot, update):
            logging.log(logging.WARNING, "Unimplemented event message_handler:")
            print("\t" + str(update))

        def chosen_inline_result_handler(bot, update):
            logging.log(logging.WARNING, "Unimplemented event chosen_inline_result_handler:")
            print("\t" + str(update))

        self.updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
        self.updater.dispatcher.add_handler(MessageHandler([], message_handler))
        self.updater.dispatcher.add_handler(ChosenInlineResultHandler(chosen_inline_result_handler))

    def inject_dependencies(self):
        self.inject_controllers()
        self.inject_models()

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def error(self, error_callback):
        self.updater.dispatcher.add_error_handler(error_callback)

    def inline_query_dispatcher(self, bot, update):
        query = update.inline_query.query
        for prog, func in self.inline_query:
            if prog.match(query):
                func(bot, update)

    def add_inline_handler(self, regex, func):
        prog = re.compile(regex)
        self.inline_query.append((prog, func))

    def inject_controllers(self):
        from telebot.controller import Controller

        for cl in get_classes('controllers'):
            if cl is not Controller and issubclass(cl, Controller):
                logging.log(logging.INFO, 'Control class is loaded %s' % cl)
                cl(self)

    def inject_models(self):
        from extentions import db
        for cl in get_classes('models'):
            if cl is not db.Entity and issubclass(cl, db.Entity):
                logging.log(logging.INFO, 'Entity class is loaded %s' % cl)

        db.generate_mapping(create_tables=True)
