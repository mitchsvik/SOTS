import random

from server.app import *
from server import views


def user_list_generator(count=20000, x_max=512, y_max=512):
    for i in range(count):
        data = {
            'x_pos': random.randint(0, x_max),
            'y_pos': random.randint(0, y_max),
        }
        yield data


user_collection = sots_instance.user_collection
if not user_collection.find_one({}):
    user_collection.insert_many([user_data for user_data in user_list_generator()])

    # In case you want to save memory (slow)
    # for user_data in user_list_generator():
    #     user_collection.insert_one(user_data)
