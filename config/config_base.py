DEBUG = False
LOCAL_SERVER_IP = '127.0.0.1'  # Your local ip-address for projects instance.
LOCAL_SERVER_PORT = '5000'  # Your local server port for project.

MYSQL_CREDENTIALS = {
    'database': 'sots',
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '',
}

MONGODB_CREDENTIALS = {
    'host': 'localhost',
    'port': 27017,
}
MONGODB_INSTANCE = 'sots'

REDIS_CREDENTIALS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True,
}
