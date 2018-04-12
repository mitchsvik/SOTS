import json
import unittest

from server.app import app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['MONGODB_INSTANCE'] = 'test_sots'
        from server.connection import user_collection
        import server.init

        self.app = app
        self.user_collection = user_collection

    def test_user_list_api(self):
        with self.app.test_client() as c:
            user_list_response = c.get('/user')
            self.assertEqual(user_list_response.status_code, 200)
            user_list = json.loads(user_list_response.data)
            self.assertEqual(len(user_list.get('response', [])), 20000)

    def test_user_api(self):
        with self.app.test_client() as c:
            user_id = 0
            self.user_collection.update_one(
                {'user_id': user_id},
                {'$set': {'x_pos': 0, 'y_pos': 0}}
            )
            user_response = c.get('/user/{user_id}'.format(user_id=user_id))
            self.assertEqual(user_response.status_code, 200)
            user_response = c.get('/user/-1')
            self.assertEqual(user_response.status_code, 404)

    def test_task_api_incorrect_timeout(self):
        with self.app.test_client() as c:
            user_id = 0
            self.user_collection.update_one(
                {'user_id': user_id},
                {'$set': {'task_list': []}}
            )

            task_response = c.post('/user/{user_id}/task'.format(user_id=user_id),
                                   data=json.dumps({'timeout': 9.99}),
                                   content_type='application/json')
            self.assertEqual(task_response.status_code, 400)
            task_response = c.post('/user/{user_id}/task'.format(user_id=user_id),
                                   data=json.dumps({'timeout': 600.01}),
                                   content_type='application/json')
            self.assertEqual(task_response.status_code, 400)
            task_response = c.post('/user/{user_id}/task'.format(user_id=user_id),
                                   data=json.dumps({'timeout': None}),
                                   content_type='application/json')
            self.assertEqual(task_response.status_code, 400)

    def test_task_api_create(self):
        with self.app.test_client() as c:
            user_id = 0
            self.user_collection.update_one(
                {'user_id': user_id},
                {'$set': {'task_list': []}}
            )

            for i in range(4):
                task_response = c.post('/user/{user_id}/task'.format(user_id=user_id),
                                       data=json.dumps({'timeout': 60}),
                                       content_type='application/json')
                self.assertEqual(task_response.status_code, 201)
            task_response = c.post('/user/{user_id}/task'.format(user_id=user_id),
                                   data=json.dumps({'timeout': 60}),
                                   content_type='application/json')
            self.assertEqual(task_response.status_code, 429)

    def test_task_delete_api(self):
        with self.app.test_client() as c:
            user_id = 0
            task_id = 'testtask1'
            self.user_collection.update_one(
                {'user_id': user_id},
                {'$set': {'x_pos': 0, 'y_pos': 0, 'task_list': [
                    {'task_id': task_id, 'task_end': 0}
                ]}}
            )

            task_response = c.delete('/user/{user_id}/task/{task_id}'.format(user_id=user_id, task_id=task_id))
            self.assertEqual(task_response.status_code, 204)
            task_response = c.delete('/user/{user_id}/task/{task_id}'.format(user_id=user_id, task_id=task_id))
            self.assertEqual(task_response.status_code, 404)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
