#!usr/bin/python
from server.init import app


if __name__ == '__main__':
    app.run(
        host=app.config['LOCAL_SERVER_IP'],
        port=int(app.config['LOCAL_SERVER_PORT']),
        debug=app.config['DEBUG']
        )
