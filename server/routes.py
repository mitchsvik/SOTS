from server.app import api

from server import views

api.add_resource(views.UserList, '/user')
api.add_resource(views.User, '/user/<int:user_id>')
api.add_resource(views.TaskList, '/user/<int:user_id>/task')
api.add_resource(views.Task, '/user/<int:user_id>/task/<string:task_id>')

# In case you want url prefix for api routes
# from server.app import app, api_blueprint
# app.register_blueprint(api_blueprint, url_prefix='/api')
