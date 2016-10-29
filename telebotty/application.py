import logging
import os
import inspect
import glob
import importlib
import re
import sys
from os.path import join

from pony.orm import Database
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler, ChosenInlineResultHandler


def get_classes(package):
    classes = []
    for file in glob.glob(join(os.path.dirname(sys.argv[0]), package, "*.py")):
        name = os.path.splitext(os.path.basename(file))[0]
        module = importlib.import_module('%s.%s' % (package, name))

        classes += [cl for name, cl in inspect.getmembers(module, inspect.isclass)]

    return classes


class Application(object):
    instance = None

    @staticmethod
    def create(token):
        if Application.instance is None:
            Application.instance = Application(token)
            Application.instance.setup_db()
        return Application.instance

    def __init__(self, token):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(InlineQueryHandler(self.inline_query_dispatcher))

        self.inline_query = []

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
        # self.updater.dispatcher.add_handler(MessageHandler([], message_handler)) TODO except commands
        self.updater.dispatcher.add_handler(ChosenInlineResultHandler(chosen_inline_result_handler))

    def setup_db(self):
        self.db = Database()
        self.db.bind('sqlite', 'db.sqlite', create_db=True)
        self.inject_models()
        self.inject_controllers()

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
        from telebotty.telebotty.controller import Controller

        for cl in get_classes('controllers'):
            if cl is not Controller and issubclass(cl, Controller):
                logging.log(logging.INFO, 'Control class is loaded %s' % cl)
                cl(self)

    def inject_models(self):
        for cl in get_classes('models'):
            if cl is not self.db.Entity and issubclass(cl, self.db.Entity):
                logging.log(logging.INFO, 'Entity class is loaded %s' % cl)

        self.db.generate_mapping(create_tables=True)
