from logging import FileHandler

from flask import Flask, Blueprint, logging
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config.config')
api = Api(app)

file_handler = FileHandler('app_log.log')
file_handler.setLevel(logging.DEBUG)
app_logger = app.logger
app_logger.setLevel(logging.DEBUG)
app_logger.addHandler(file_handler)

# In case you want url prefix for api routes
# api_blueprint = Blueprint('API', 'api')
# api = Api(api_blueprint)
