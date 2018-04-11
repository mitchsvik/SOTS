import time
import uuid

from flask import request
from flask_restful import Resource

from server.app import user_collection


def remove_object_id(instance):
    instance.pop('_id')
    return instance


class UserList(Resource):
    """
    Show a list of all users personal data for current session
    """
    def get(self):
        user_data_list = user_collection.find({})
        return {'response': [{'user_id': user_data.get('user_id', 0)} for user_data in user_data_list]}


class User(Resource):
    """
    Show a single user field of view
    """
    def get(self, user_id):
        user = user_collection.find_one({'user_id': user_id})
        user_in_area = user_collection.find({
            'x_pos': {'$lt': user['x_pos'] + 32, '$gt': user['x_pos'] - 32},
            'y_pos': {'$lt': user['y_pos'] + 32, '$gt': user['y_pos'] - 32},
        })
        response = [remove_object_id(user_data) for user_data in user_in_area]
        return {'response': response}


class TaskList(Resource):
    """
    Add user task
    """
    def post(self, user_id):
        request_data = request.get_json()
        task_end = time.time() + request_data['timeout']
        task_id = uuid.uuid4().hex
        user_collection.update_one(
            {'user_id': user_id},
            {'$push': {'task_list': {'task_id': task_id, 'task_end': task_end}}}
        )
        return {'response': task_id}, 201


class Task(Resource):
    """
    Delete user task
    """
    def delete(self, user_id, task_id):
        user_collection.update_one(
            {'user_id': user_id},
            {'$pull': {'task_list': {'task_id': task_id}}}
        )
        return '', 204
