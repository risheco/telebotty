import logging
import os
import inspect
import glob
import importlib
import sys
from os.path import join

from pony.orm import Database
from telebotty.telebotty.handler import Handler


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
        self.db = Database()
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        self.handler = Handler(token)

    def setup_db(self):
        self.db.bind('sqlite', 'db.sqlite', create_db=True)
        self.inject_models()
        self.inject_controllers()

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
