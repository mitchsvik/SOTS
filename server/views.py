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
        return {'response': [{'user_id': user_data.get('user_id', None)} for user_data in user_data_list]}


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
        timeout = request_data.get('timeout', None)
        if timeout is None:
            return {'error': "field 'timeout' is required for this request"}, 400
        if not 10 <= timeout <= 600:
            return {'error': "'timeout' should be between 10 and 600 seconds. Got {timeout}"
                    .format(timeout=timeout)}, 400

        task_end = time.time() + timeout
        task_id = uuid.uuid4().hex
        update_data = user_collection.update_one(
            {'user_id': user_id, 'task_list.3': {'$exists': False}},
            {'$push': {'task_list': {'task_id': task_id, 'task_end': task_end}}}
        )

        if update_data.modified_count == 1:
            return {'response': task_id}, 201
        else:
            return {'error': "Reached the limit of task list size"}, 429


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
