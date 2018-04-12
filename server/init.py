import random

import pymongo

from server.app import app
from server.connection import sots_instance
from server import routes


def user_list_generator(count=20000, x_max=512, y_max=512):
    for i in range(count):
        data = {
            'x_pos': random.randint(0, x_max),
            'y_pos': random.randint(0, y_max),
            'user_id': i,
            'task_list': []
        }
        yield data


user_collection = sots_instance.user_collection
if not user_collection.find_one({}):
    user_collection.insert_many(user_list_generator())
    user_collection.create_index([('user_id', pymongo.ASCENDING)], unique=True)
