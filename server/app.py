import flask

import peewee
import pymongo
import redis


app = flask.Flask(__name__)
app.config.from_object('config.config')

client_mysql = peewee.MySQLDatabase(**app.config['MYSQL_CREDENTIALS'])
client_mongo = pymongo.MongoClient(**app.config['MONGODB_CREDENTIALS'])
client_redis = redis.StrictRedis(**app.config['REDIS_CREDENTIALS'])

sots_instance = client_mongo[app.config.get('MONGODB_INSTANCE', 'sots')]
