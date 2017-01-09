import logging

import re
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler, ChosenInlineResultHandler


class Handler(Updater):
    def __init__(self, token):
        super().__init__(token)

        self.dispatcher.add_handler(InlineQueryHandler(self.inline_query_dispatcher))

        self.inline_query = []
        self.text_message = []

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

        self.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
        self.dispatcher.add_handler(ChosenInlineResultHandler(chosen_inline_result_handler))

    def inline_query_dispatcher(self, bot, update):
        query = update.inline_query.query
        for prog, func in self.inline_query:
            if prog.match(query):
                func(bot, update)

    def add_inline_handler(self, regex, func):
        prog = re.compile(regex)
        self.inline_query.append((prog, func))

    def error(self, error_callback):
        self.dispatcher.add_error_handler(error_callback)

    def run(self):
        self.start_polling()
        self.idle()
