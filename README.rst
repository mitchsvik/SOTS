Simple Online Task Server (SOTS)
================================

Server managing
---------------

To start server
    $ python run.py
To run tests
    $ python tests.py

Available API
-------------

* /task : 'GET' - returns list of user ids
* /task/<user_id>: 'GET' - returns user point of view
* /task/<user_id>/task: 'POST' - creates new task, returns new task_id, 'timeout' parameter required
* /task/<user_id>/task/<task_id>: 'DELETE' - deletes task by task_id, returns nothing
