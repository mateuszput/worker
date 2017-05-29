import psutil
import subprocess

import os
import threading
from time import sleep, time

import requests


TIME_STEP = 1
WATCHER_IP = "http://0.0.0.0"
WATCHER_STEP = "/proc/step"

SERVER_IP = "http://localhost:50123"
SERVER_END = "/task/{}/end"   # SERVER_END.format(taskID)


class Monitor(threading.Thread):

    def __init__(self, taskID, task_array):
        threading.Thread.__init__(self)
        self.taskID = taskID
        self.task_array = task_array

        filename = "./outputs/{}".format(taskID)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        self.output = open(filename, "w")

    def run(self):
        pid = self._run_task()

        p = psutil.Process(pid)
        while psutil.pid_exists(pid) and p.status() != "zombie":
            try:

                proc_info = p.as_dict(attrs=[
                    'cpu_percent',
                    'cpu_times',
                    'status',
                    'num_threads',
                    'memory_full_info',
                    'io_counters'
                ])
                proc_info['cpu_times'] = dict(proc_info['cpu_times']._asdict())
                proc_info['memory_full_info'] = dict(proc_info['memory_full_info']._asdict())
                proc_info['io_counters'] = dict(proc_info['io_counters']._asdict())

                proc_info['id'] = self.taskID
                proc_info['timestamp'] = time()

                # add task info

            except Exception as e:
                print "Process probably exited.", e
                break

            self._send_proc_info(proc_info)
            sleep(TIME_STEP)

        self.output.close()
        self._send_end_info()


    def _run_task(self):
        p = subprocess.Popen(self.task_array, stdout=self.output)
        return p.pid

    def _send_proc_info(self, proc_info):
        print proc_info
        print

        watcher_url = WATCHER_IP + WATCHER_STEP
        try:
            response = requests.post(watcher_url, data=proc_info)
        except requests.exceptions.ConnectionError as e:
            print e
            # TODO: store proc_info for later post


    def _send_end_info(self):
        server_url = SERVER_IP + SERVER_END.format(self.taskID)
        data = "some data"

        while True:
            try:
                response = requests.post(server_url, data=data)
            except requests.exceptions.ConnectionError as e:
                print e

                sleep(1)
                continue
            break



if __name__ == '__main__':
    taskID = 1
    task = ["python2.7", "monte_carlo.py", "" + str(taskID)]

    monitor = Monitor(taskID, task)
    monitor.start()
