from flask import Flask, Blueprint
from flask_restful import Api

import peewee
import pymongo
import redis


app = Flask(__name__)
app.config.from_object('config.config')
api = Api(app)

# In case you want url prefix for api routes
# api_blueprint = Blueprint('API', 'api')
# api = Api(api_blueprint)

client_mysql = peewee.MySQLDatabase(**app.config['MYSQL_CREDENTIALS'])
client_mongo = pymongo.MongoClient(**app.config['MONGODB_CREDENTIALS'])
client_redis = redis.StrictRedis(**app.config['REDIS_CREDENTIALS'])

sots_instance = client_mongo[app.config.get('MONGODB_INSTANCE', 'sots')]
user_collection = sots_instance.user_collection
