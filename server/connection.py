from queue import Queue

import peewee
import pymongo
import redis

from server.app import app
from server.taskmanager import TaskManager


client_mysql = peewee.MySQLDatabase(**app.config['MYSQL_CREDENTIALS'])
client_mongo = pymongo.MongoClient(**app.config['MONGODB_CREDENTIALS'])
client_redis = redis.StrictRedis(**app.config['REDIS_CREDENTIALS'])

sots_instance = client_mongo[app.config.get('MONGODB_INSTANCE', 'sots')]
user_collection = sots_instance.user_collection

task_queue = Queue()
task_manager = TaskManager(queue=task_queue)
task_manager.start()
