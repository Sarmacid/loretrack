from flask import Flask
import logging
from logging.handlers import RotatingFileHandler


def config_logs(app):
    logging_level = 'DEBUG'
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('/tmp/loretrack.log', maxBytes=10000, backupCount=1)
    logging.getLogger().setLevel(logging_level)
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


app = Flask(__name__)
app.config.from_object('loretrack.config.Flask_config')
#config_logs(app)

import views
