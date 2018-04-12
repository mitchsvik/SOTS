import time
import uuid

from flask import request
from flask_restful import Resource

from server.app import user_collection, task_queue, app_logger


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
        if user is None:
            return {'error': 'User with id={} does not exists'.format(user_id)}, 404
        user_in_area = user_collection.find({
            'x_pos': {'$lt': user['x_pos'] + 16, '$gt': user['x_pos'] - 16},
            'y_pos': {'$lt': user['y_pos'] + 16, '$gt': user['y_pos'] - 16},
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
            return {'error': "Field 'timeout' is required for this request"}, 400
        if not 10 <= timeout <= 600:
            return {'error': "Field 'timeout' should be between 10 and 600 seconds. Got {timeout}"
                    .format(timeout=timeout)}, 400

        task_end = time.time() + timeout
        task_id = uuid.uuid4().hex
        update_data = user_collection.update_one(
            {'user_id': user_id, 'task_list.3': {'$exists': False}},
            {'$push': {'task_list': {'task_id': task_id, 'task_end': task_end}}}
        )

        if update_data.modified_count == 1:
            # Task signature ['time', 'user_id', 'task_id', 'is_active']
            task = (task_end, user_id, task_id, True)
            task_queue.put(task)
            app_logger.info('Created task by user {1} with id {2}, expires at {0}'.format(*task))
            return {'response': task_id}, 201
        else:
            return {'error': "Reached the limit of task list size"}, 429


class Task(Resource):
    """
    Delete user task
    """
    def delete(self, user_id, task_id):
        user_data = user_collection.find_one({'user_id': user_id})
        matched_task = list(filter(lambda t: t.get('task_id') == task_id, user_data.get('task_list', [])))

        updated_data = user_collection.update_one(
            {'user_id': user_id},
            {'$pull': {'task_list': {'task_id': task_id}}}
        )
        if updated_data.modified_count == 1:
            task_end = matched_task[0].get('task_end')
            # Task signature ['time', 'user_id', 'task_id', 'is_active']
            task = (task_end, user_id, task_id, False)
            task_queue.put(task)
            app_logger.info('Removed task by user {1} with id {2}'.format(*task))
            return '', 204
        else:
            return {'error': 'Task not found or already expired'}, 404
