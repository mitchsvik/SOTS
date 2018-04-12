from logging import FileHandler
from queue import Queue

from flask import Flask, Blueprint, logging
from flask_restful import Api

import peewee
import pymongo
import redis

from server.taskmanager import TaskManager


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

client_mysql = peewee.MySQLDatabase(**app.config['MYSQL_CREDENTIALS'])
client_mongo = pymongo.MongoClient(**app.config['MONGODB_CREDENTIALS'])
client_redis = redis.StrictRedis(**app.config['REDIS_CREDENTIALS'])

sots_instance = client_mongo[app.config.get('MONGODB_INSTANCE', 'sots')]
user_collection = sots_instance.user_collection

task_queue = Queue()
task_manager = TaskManager(queue=task_queue)
task_manager.start()
