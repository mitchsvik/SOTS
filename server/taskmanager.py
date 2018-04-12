import threading
import time
import queue


class TaskManager(threading.Thread):
    _sleep = staticmethod(time.sleep)

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from server.app import user_collection

        self.queue = queue
        # self.daemon = True
        self.task_list = []
        self.user_collection = user_collection
        self.populate_from_collection()

    def populate_from_collection(self):
        user_cursor = self.user_collection.find()
        for user in user_cursor:
            for user_task in user.get('task_list'):
                task = (user_task['task_end'], user['user_id'], user_task['task_id'])
                self.task_list.append(task)
        self.task_list.sort(key=lambda t: t[0])
        print(list(self.task_list))

    def pull_task(self):
        # pull new tasks from queue
        # since we sleep less or equal to 10 second active or just finished tasks will be got
        while True:
            try:
                # Task signature ['time', 'user_id', 'task_id', 'is_active']
                task = self.queue.get(block=False)
            except queue.Empty as e:
                break

            print(task)
            valuable_slice = task[:3]
            task_is_active = task[3]
            # must update task list before proceed
            # new and deleted tasks can be got from queue
            if task_is_active:
                # keep task list sorted may be faster than sort every timer cycle
                for i, task_in_list in enumerate(self.task_list):
                    if task_in_list[0] > valuable_slice[0]:
                        self.task_list.insert(i, valuable_slice)
                        break
                else:
                    self.task_list.append(valuable_slice)
            else:
                self.task_list.remove(valuable_slice)

    def run(self):
        while True:
            self.pull_task()
            # sort active task list by task end time
            # sort list every cycle is overwork. List must be sorted all the time
            # self.task_list.sort(key=lambda t: t[0])

            now = time.time()
            expired_list = list(filter(lambda t: t[0] <= now, self.task_list))
            for expired_task in expired_list:
                self.user_collection.update_one(
                    {'user_id': expired_task[1]},
                    {'$pull': {'task_list': {'task_id': expired_task[2]}}}
                )

            self.task_list = self.task_list[len(expired_list):]
            until_next_task = (self.task_list[0][0] - now) if len(self.task_list) > 0 else 10
            until_next_task = 10 if until_next_task > 10 else until_next_task
            # try to catch more than one task after wake up. Limits max possible updates/second
            self._sleep(until_next_task + 0.005)
